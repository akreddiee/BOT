import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from app.storage.json_storage import storage
from app.utils.logger import get_logger

logger = get_logger("ContextService")


class ContextService:
    def __init__(self):
        self.storage = storage

    def push_context(
        self, scope: str, context_id: str, version: int, payload: Dict[str, Any]
    ) -> Tuple[bool, int, str]:
        """Push a context object into storage with scope validation."""
        valid_scopes = {"category", "merchant", "customer", "trigger"}
        if scope not in valid_scopes:
            return False, 0, f"Invalid scope: {scope}"
        return self.storage.push_context(scope, context_id, version, payload)

    def get_context(self, scope: str, context_id: str) -> Optional[Dict[str, Any]]:
        return self.storage.get_context(scope, context_id)

    def get_context_counts(self) -> Dict[str, int]:
        return self.storage.get_context_counts()

    def get_uptime_seconds(self) -> int:
        return self.storage.get_uptime_seconds()

    def load_seed_data(self, seed_dir: str = "dataset") -> None:
        """Seed datasets on startup if available using safe file context managers."""
        path = Path(seed_dir)
        if not path.exists():
            path = Path("dataset/expanded")
        if not path.exists():
            return

        logger.info(f"Loading seed data from {path}")
        # Load categories
        cat_dir = path / "categories"
        if cat_dir.exists():
            for f in cat_dir.glob("*.json"):
                try:
                    with open(f, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                    slug = data.get("slug", f.stem)
                    self.push_context("category", slug, 1, data)
                except Exception as e:
                    logger.warning(f"Failed to load category seed {f}: {e}")

        # Load merchants seed
        merchants_seed = path / "merchants_seed.json"
        if merchants_seed.exists():
            try:
                with open(merchants_seed, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                for m in data.get("merchants", []):
                    mid = m.get("merchant_id")
                    if mid:
                        self.push_context("merchant", mid, 1, m)
            except Exception as e:
                logger.warning(f"Failed to load merchants seed: {e}")

        # Load merchants dir
        merchants_dir = path / "merchants"
        if merchants_dir.exists():
            for f in merchants_dir.glob("*.json"):
                try:
                    with open(f, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                    mid = data.get("merchant_id", f.stem)
                    self.push_context("merchant", mid, 1, data)
                except Exception as e:
                    logger.warning(f"Failed to load merchant file {f}: {e}")

        # Load customers seed
        customers_seed = path / "customers_seed.json"
        if customers_seed.exists():
            try:
                with open(customers_seed, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                for c in data.get("customers", []):
                    cid = c.get("customer_id")
                    if cid:
                        self.push_context("customer", cid, 1, c)
            except Exception as e:
                logger.warning(f"Failed to load customers seed: {e}")

        # Load customers dir
        customers_dir = path / "customers"
        if customers_dir.exists():
            for f in customers_dir.glob("*.json"):
                try:
                    with open(f, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                    cid = data.get("customer_id", f.stem)
                    self.push_context("customer", cid, 1, data)
                except Exception as e:
                    logger.warning(f"Failed to load customer file {f}: {e}")

        # Load triggers seed
        triggers_seed = path / "triggers_seed.json"
        if triggers_seed.exists():
            try:
                with open(triggers_seed, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                for t in data.get("triggers", []):
                    tid = t.get("id")
                    if tid:
                        self.push_context("trigger", tid, 1, t)
            except Exception as e:
                logger.warning(f"Failed to load triggers seed: {e}")

        # Load triggers dir
        triggers_dir = path / "triggers"
        if triggers_dir.exists():
            for f in triggers_dir.glob("*.json"):
                try:
                    with open(f, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                    tid = data.get("id", f.stem)
                    self.push_context("trigger", tid, 1, data)
                except Exception as e:
                    logger.warning(f"Failed to load trigger file {f}: {e}")


context_service = ContextService()
