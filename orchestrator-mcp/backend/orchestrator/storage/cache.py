import time
from hashlib import sha256
from typing import Any, Dict


class SimpleCache:
    def __init__(self):
        self.store: Dict[str, tuple[float, Any]] = {}

    def _key(self, tool: str, args: Dict[str, Any]) -> str:
        payload = tool + str(sorted(args.items()))
        return sha256(payload.encode()).hexdigest()

    def get(self, tool: str, args: Dict[str, Any]) -> Any | None:
        key = self._key(tool, args)
        record = self.store.get(key)
        if not record:
            return None
        expires, value = record
        if time.time() > expires:
            del self.store[key]
            return None
        return value

    def set(self, tool: str, args: Dict[str, Any], value: Any, ttl: int = 60):
        key = self._key(tool, args)
        self.store[key] = (time.time() + ttl, value)
