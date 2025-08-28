from typing import Any, Dict, List
from dataclasses import dataclass, field


@dataclass
class AuditEntry:
    user: str
    tool: str
    args: str
    result: str
    ok: bool
    latency_ms: float


class AuditLogger:
    def __init__(self):
        self.entries: List[AuditEntry] = []

    def log(self, user: str, tool: str, args: Dict[str, Any], result: Any, ok: bool, latency_ms: float):
        self.entries.append(
            AuditEntry(
                user=user,
                tool=tool,
                args=str(args),
                result=str(result),
                ok=ok,
                latency_ms=latency_ms,
            )
        )
