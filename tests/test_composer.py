import pytest
from app.services.composer_service import composer_service


def test_composer_dentist_research_digest():
    cat = {"slug": "dentists"}
    merchant = {
        "merchant_id": "m_001",
        "category_slug": "dentists",
        "identity": {"name": "Dr. Meera Clinic", "owner_first_name": "Meera", "locality": "Lajpat Nagar"},
        "customer_aggregate": {"high_risk_adult_count": 124},
    }
    trg = {
        "id": "trg_001",
        "kind": "research_digest",
        "scope": "merchant",
        "payload": {
            "top_item": {
                "title": "3-month fluoride recall cuts caries 38% better",
                "source": "JIDA Oct 2026, p.14",
                "trial_n": 2100,
            }
        },
    }
    res = composer_service.compose(cat, merchant, trg)
    assert res["send_as"] == "vera"
    assert "Dr. Meera" in res["body"]
    assert "38%" in res["body"]
    assert "2,100" in res["body"]
    assert "JIDA Oct 2026" in res["body"]
    assert res["cta"] == "open_ended"


def test_composer_customer_facing_recall():
    cat = {"slug": "dentists"}
    merchant = {
        "merchant_id": "m_001",
        "category_slug": "dentists",
        "identity": {"name": "Dr. Meera's Clinic", "locality": "Delhi"},
    }
    trg = {"id": "trg_recall", "kind": "recall_due", "scope": "customer"}
    cust = {
        "customer_id": "c_001",
        "identity": {"name": "Priya", "language_pref": "hi-en mix"},
    }
    res = composer_service.compose(cat, merchant, trg, cust)
    assert res["send_as"] == "merchant_on_behalf"
    assert "Priya" in res["body"]
    assert "Dr. Meera" in res["body"]
    assert "2 slots" in res["body"] or "slots" in res["body"]


def test_composer_all_categories():
    categories = ["dentists", "salons", "restaurants", "gyms", "pharmacies"]
    for slug in categories:
        cat = {"slug": slug}
        merchant = {
            "merchant_id": f"m_{slug}",
            "category_slug": slug,
            "identity": {"name": f"Test {slug.capitalize()}", "owner_first_name": "Owner", "locality": "Sector 1"},
            "performance": {"views": 1500, "calls": 25},
        }
        trg = {"id": f"trg_{slug}", "kind": "perf_dip", "scope": "merchant"}
        res = composer_service.compose(cat, merchant, trg)
        assert len(res["body"]) > 20
        assert res["send_as"] == "vera"
        assert res["cta"] in ("binary_yes_no", "open_ended", "multi_choice_slot", "binary_confirm_cancel")
