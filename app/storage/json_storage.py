import json
import os
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger("JSONStorage")


class JSONStorage:
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or settings.DATA_DIR).resolve()
        self.start_time = time.time()
        self._lock = threading.Lock()
        self._contexts: Dict[Tuple[str, str], Dict[str, Any]] = {}
        self._conversations: Dict[str, list] = {}
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        """Create storage directories under /data."""
        try:
            with self._lock:
                for sub in ["category", "merchant", "customer", "trigger", "conversations"]:
                    (self.data_dir / sub).mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create storage directories: {e}")

    def clear(self) -> None:
        """Clear in-memory caches (for test isolation)."""
        with self._lock:
            self._contexts.clear()
            self._conversations.clear()

    def get_uptime_seconds(self) -> int:
        return int(time.time() - self.start_time)

    def push_context(
        self, scope: str, context_id: str, version: int, payload: Dict[str, Any]
    ) -> Tuple[bool, int, str]:
        """
        Store context object atomically. Thread-safe.
        Idempotent by (scope, context_id, version). Re-posting same version is a no-op (returns accepted=True).
        Only strictly lower versions return stale_version.
        """
        key = (scope, context_id)
        with self._lock:
            existing = self._contexts.get(key)
            if existing and version < existing["version"]:
                return False, existing["version"], "stale_version"

            entry = {"version": version, "payload": payload, "updated_at": time.time()}
            self._contexts[key] = entry

            # Persist to disk under lock
            try:
                scope_dir = self.data_dir / scope
                scope_dir.mkdir(parents=True, exist_ok=True)
                file_path = scope_dir / f"{context_id}.json"
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(entry, f, indent=2, ensure_ascii=False)
            except Exception as e:
                logger.warning(f"Failed to persist context {scope}/{context_id}: {e}")

            return True, version, "ok"

    def get_context(self, scope: str, context_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve stored context payload."""
        key = (scope, context_id)
        with self._lock:
            entry = self._contexts.get(key)
            if entry:
                return entry["payload"]

            # Fallback to disk if not in memory
            file_path = self.data_dir / scope / f"{context_id}.json"
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        entry = json.load(f)
                        self._contexts[key] = entry
                        return entry.get("payload")
                except Exception as e:
                    logger.error(f"Failed to read disk context {file_path}: {e}")
        return None

    def get_context_counts(self) -> Dict[str, int]:
        """Return count of loaded contexts per scope."""
        counts = {"category": 0, "merchant": 0, "customer": 0, "trigger": 0}
        with self._lock:
            for (scope, _), _ in self._contexts.items():
                if scope in counts:
                    counts[scope] += 1
        return counts

    def record_turn(self, conversation_id: str, turn_data: Dict[str, Any]) -> None:
        """Record conversation turn in thread-safe manner."""
        with self._lock:
            if conversation_id not in self._conversations:
                self._conversations[conversation_id] = []
            self._conversations[conversation_id].append(turn_data)

    def get_conversation_history(self, conversation_id: str) -> list:
        with self._lock:
            return list(self._conversations.get(conversation_id, []))


storage = JSONStorage()
