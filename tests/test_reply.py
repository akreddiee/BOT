import pytest
from app.services.reply_service import reply_service


def test_reply_auto_reply_detection():
    # Turn 1 auto-reply -> wait action
    res1 = reply_service.handle_reply(
        conversation_id="conv_auto_test",
        merchant_id="m_001",
        customer_id=None,
        from_role="merchant",
        message="Thank you for contacting us! Our team will respond shortly.",
        received_at="2026-04-26T10:00:00Z",
        turn_number=1,
    )
    assert res1["action"] == "wait"
    assert res1["wait_seconds"] == 14400

    # Turn 3 auto-reply -> end action
    res3 = reply_service.handle_reply(
        conversation_id="conv_auto_test",
        merchant_id="m_001",
        customer_id=None,
        from_role="merchant",
        message="Thank you for contacting us! Our team will respond shortly.",
        received_at="2026-04-26T10:00:00Z",
        turn_number=3,
    )
    assert res3["action"] == "end"


def test_reply_hostile_optout():
    res = reply_service.handle_reply(
        conversation_id="conv_hostile_test",
        merchant_id="m_001",
        customer_id=None,
        from_role="merchant",
        message="Stop messaging me. This is useless spam.",
        received_at="2026-04-26T10:00:00Z",
        turn_number=2,
    )
    assert res["action"] == "end"


def test_reply_intent_commitment():
    res = reply_service.handle_reply(
        conversation_id="conv_intent_test",
        merchant_id="m_001",
        customer_id=None,
        from_role="merchant",
        message="Ok lets do it. Whats next?",
        received_at="2026-04-26T10:00:00Z",
        turn_number=2,
    )
    assert res["action"] == "send"
    assert "Done" in res["body"] or "Sending" in res["body"] or "schedule" in res["body"]


def test_reply_off_topic_gst():
    res = reply_service.handle_reply(
        conversation_id="conv_off_topic_test",
        merchant_id="m_001",
        customer_id=None,
        from_role="merchant",
        message="Can you also help me with my GST filing this month?",
        received_at="2026-04-26T10:00:00Z",
        turn_number=2,
    )
    assert res["action"] == "send"
    assert "GST" in res["body"]
    assert "CA" in res["body"]
