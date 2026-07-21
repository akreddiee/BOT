import re
from typing import List, Tuple
from app.utils.text_helpers import contains_any, normalize_text
from app.utils.logger import get_logger

logger = get_logger("DetectorService")

# Canned auto-reply phrases common in WhatsApp Business
AUTO_REPLY_PATTERNS = [
    "thank you for contacting",
    "thanks for reaching out",
    "our team will respond",
    "we will get back to you",
    "aapki jaankari ke liye",
    "main aapki yeh sabhi baatein",
    "main ek automated assistant hoon",
    "automated assistant",
    "we are currently unavailable",
    "business hours are",
    "hum abhi uplabdh nahi hain",
    "shukriya contact karne ke liye",
]

HOSTILE_PATTERNS = [
    "stop messaging",
    "stop sending",
    "useless spam",
    "don't message me",
    "dont message me",
    "not interested",
    "remove me",
    "unsubscribe",
    "leave me alone",
    "stop this",
    "bothering me",
    "don't contact",
    "dont contact",
]

COMMITMENT_PATTERNS = [
    "yes",
    "ok lets do it",
    "ok let's do it",
    "whats next",
    "what's next",
    "go ahead",
    "send me the abstract",
    "send abstract",
    "draft the patient",
    "draft it",
    "proceed",
    "sure",
    "let's start",
    "lets start",
    "judrna hai",
    "want to join",
    "confirm",
    "do it",
    "ha",
    "thik hai",
    "kar do",
    "send it",
]

OFF_TOPIC_PATTERNS = [
    "gst",
    "tax",
    "income tax",
    "ca",
    "audit",
    "accounting",
    "legal dispute",
]


class DetectorService:
    @staticmethod
    def is_auto_reply(message: str, history: List[dict] = None) -> bool:
        """Detect automated responses or repeated identical messages."""
        norm = normalize_text(message)
        if contains_any(norm, AUTO_REPLY_PATTERNS):
            return True

        if history:
            merchant_msgs = [
                h.get("message", "") for h in history if h.get("from") in ("merchant", "customer")
            ]
            # Must be at least 2 merchant messages, and the last 2 must be identical text
            if len(merchant_msgs) >= 2 and merchant_msgs[-1] == message and merchant_msgs[-2] == message:
                return True
        return False

    @staticmethod
    def is_hostile_or_optout(message: str) -> bool:
        """Detect if merchant wants to stop or is hostile."""
        return contains_any(message, HOSTILE_PATTERNS)

    @staticmethod
    def is_intent_commitment(message: str) -> bool:
        """Detect explicit intent / commitment from merchant."""
        return contains_any(message, COMMITMENT_PATTERNS)

    @staticmethod
    def is_off_topic(message: str) -> Tuple[bool, str]:
        """Detect off-topic requests like GST filing."""
        for pattern in OFF_TOPIC_PATTERNS:
            if pattern in message.lower():
                return True, pattern
        return False, ""


detector_service = DetectorService()
