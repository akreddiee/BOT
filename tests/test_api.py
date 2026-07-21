import pytest
from fastapi.testclient import TestClient
from main import app
from app.storage.json_storage import storage

client = TestClient(app)


def test_healthz():
    response = client.get("/v1/healthz")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "uptime_seconds" in data
    assert "contexts_loaded" in data
    assert "category" in data["contexts_loaded"]
    assert "merchant" in data["contexts_loaded"]
    assert "customer" in data["contexts_loaded"]
    assert "trigger" in data["contexts_loaded"]


def test_metadata():
    response = client.get("/v1/metadata")
    assert response.status_code == 200
    data = response.json()
    assert "team_name" in data
    assert "model" in data
    assert "version" in data


def test_push_context_and_idempotency():
    payload = {
        "slug": "dentists",
        "voice": {"tone": "clinical"},
        "peer_stats": {"avg_rating": 4.4},
    }

    ctx_id = "dentists_api_test_unique"

    # Version 1 first push -> 200 OK
    req1 = {
        "scope": "category",
        "context_id": ctx_id,
        "version": 1,
        "payload": payload,
        "delivered_at": "2026-04-26T10:00:00Z",
    }
    res1 = client.post("/v1/context", json=req1)
    assert res1.status_code == 200
    assert res1.json()["accepted"] is True

    # Re-push version 1 (same version) -> 200 OK (idempotent no-op)
    res2 = client.post("/v1/context", json=req1)
    assert res2.status_code == 200
    assert res2.json()["accepted"] is True

    # Push higher version (version 2) -> 200 OK
    req2 = dict(req1, version=2)
    res3 = client.post("/v1/context", json=req2)
    assert res3.status_code == 200
    assert res3.json()["accepted"] is True

    # Push lower version (version 1 when stored version is 2) -> 409 Conflict
    res4 = client.post("/v1/context", json=req1)
    assert res4.status_code == 409
    assert res4.json()["accepted"] is False
    assert res4.json()["reason"] == "stale_version"
    assert res4.json()["current_version"] == 2


def test_tick_and_reply():
    # Push merchant and trigger
    m_req = {
        "scope": "merchant",
        "context_id": "m_test_api_001",
        "version": 1,
        "payload": {
            "merchant_id": "m_test_api_001",
            "category_slug": "dentists",
            "identity": {"name": "Test Clinic", "owner_first_name": "Meera", "locality": "Saket"},
            "performance": {"views": 1000, "ctr": 0.02},
        },
        "delivered_at": "2026-04-26T10:00:00Z",
    }
    client.post("/v1/context", json=m_req)

    t_req = {
        "scope": "trigger",
        "context_id": "trg_test_api_001",
        "version": 1,
        "payload": {
            "id": "trg_test_api_001",
            "scope": "merchant",
            "kind": "research_digest",
            "merchant_id": "m_test_api_001",
            "payload": {"top_item": {"title": "Fluoride recall study", "source": "JIDA 2026"}},
        },
        "delivered_at": "2026-04-26T10:00:00Z",
    }
    client.post("/v1/context", json=t_req)

    # Tick call
    tick_res = client.post(
        "/v1/tick", json={"now": "2026-04-26T10:05:00Z", "available_triggers": ["trg_test_api_001"]}
    )
    assert tick_res.status_code == 200
    actions = tick_res.json()["actions"]
    assert len(actions) == 1
    assert actions[0]["merchant_id"] == "m_test_api_001"
    assert len(actions[0]["body"]) > 0

    # Reply call (Intent commitment)
    reply_req = {
        "conversation_id": actions[0]["conversation_id"],
        "merchant_id": "m_test_api_001",
        "customer_id": None,
        "from_role": "merchant",
        "message": "Yes please send the abstract",
        "received_at": "2026-04-26T10:10:00Z",
        "turn_number": 2,
    }
    reply_res = client.post("/v1/reply", json=reply_req)
    assert reply_res.status_code == 200
    assert reply_res.json()["action"] == "send"
