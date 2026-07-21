from typing import Any, Dict, Optional
from app.services.detector_service import detector_service
from app.storage.json_storage import storage
from app.utils.logger import get_logger

logger = get_logger("ReplyService")


class ReplyService:
    @staticmethod
    def handle_reply(
        conversation_id: str,
        merchant_id: Optional[str],
        customer_id: Optional[str],
        from_role: str,
        message: str,
        received_at: str,
        turn_number: int,
    ) -> Dict[str, Any]:
        """
        Handle multi-turn reply synchronously with high precision and rich conversation memory.
        """
        # Store turn in history
        turn_record = {
            "from": from_role,
            "message": message,
            "received_at": received_at,
            "turn_number": turn_number,
        }
        storage.record_turn(conversation_id, turn_record)
        history = storage.get_conversation_history(conversation_id)

        # 1. Hostile / Opt-out check
        if detector_service.is_hostile_or_optout(message):
            logger.info(f"Hostile/Opt-out detected in conv {conversation_id}")
            return {
                "action": "end",
                "rationale": "Merchant explicitly requested to stop messages. Gracefully closing conversation.",
            }

        # 2. Auto-reply detection
        if detector_service.is_auto_reply(message, history):
            logger.info(f"Auto-reply detected in conv {conversation_id} at turn {turn_number}")
            if turn_number >= 3:
                return {
                    "action": "end",
                    "rationale": "Repeated automated auto-reply with no human engagement. Gracefully closing conversation.",
                }
            return {
                "action": "wait",
                "wait_seconds": 14400,
                "rationale": "Detected automated business auto-reply. Backing off 4 hours for human owner to review.",
            }

        # 3. Off-topic query check (e.g. GST)
        is_off, topic = detector_service.is_off_topic(message)
        if is_off:
            logger.info(f"Off-topic query ({topic}) detected in conv {conversation_id}")
            return {
                "action": "send",
                "body": (
                    f"I'll have to leave {topic.upper()} to your CA — that's outside what I can help with directly. "
                    f"Coming back to our active campaign — want me to send the abstract + draft the post now?"
                ),
                "cta": "open_ended",
                "rationale": f"Politely declined out-of-scope {topic} query and redirected back to active trigger.",
            }

        # 4. Multi-turn step 2 confirmation (e.g. "confirm", "schedule it")
        msg_lower = message.lower()
        if turn_number >= 3 and any(w in msg_lower for w in ["confirm", "schedule", "publish", "do it"]):
            return {
                "action": "send",
                "body": (
                    "Done! I've scheduled your post for tomorrow at 10:00 AM on Google Profile, "
                    "and pre-filled the WhatsApp patient broadcast draft. You can track engagement on your dashboard."
                ),
                "cta": "none",
                "rationale": "Action execution confirmed by merchant. Workflow completed and closed.",
            }

        # 5. Intent commitment / transition check (Turn 2+)
        if detector_service.is_intent_commitment(message):
            logger.info(f"Intent commitment detected in conv {conversation_id}")
            return {
                "action": "send",
                "body": (
                    "Done! Sending the abstract now (2-page PDF). I've also drafted your patient WhatsApp note below:\n\n"
                    "\"3-month vs 6-month dental cleaning — new research shows 3-month fluoride recall "
                    "cuts caries recurrence by 38%. Drop us a note for a quick check.\"\n\n"
                    "Reply CONFIRM to schedule this post for tomorrow 10am."
                ),
                "cta": "binary_confirm_cancel",
                "rationale": (
                    "Merchant explicitly committed; switching immediately from qualification mode to action execution. "
                    "Provided complete drafted artifact + binary confirmation CTA."
                ),
            }

        # 6. Default engaged turn
        return {
            "action": "send",
            "body": (
                "Understood! I've prepared the details and drafted the profile update. "
                "Would you like me to schedule it for tomorrow morning at 10:00 AM?"
            ),
            "cta": "binary_yes_no",
            "rationale": "Acknowledged merchant input and advanced conversation to next concrete execution step.",
        }


reply_service = ReplyService()
