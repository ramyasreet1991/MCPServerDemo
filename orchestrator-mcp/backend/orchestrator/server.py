import time
from typing import Any, Dict

from .clients.mcp_hub import load_hub
from .policy.engine import PolicyEngine
from .storage.cache import SimpleCache
from .storage.audit import AuditLogger
from .util.redaction import redact_inputs, redact_outputs
from .util.settings import load_yaml, settings


class ToolRegistry:
    def __init__(self):
        self.hub = load_hub()
        policy_data = load_yaml(settings.policy_file)
        self.policy = PolicyEngine(policy_data)
        self.cache = SimpleCache()
        self.audit = AuditLogger()

    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        tools = {}
        for vendor, defs in self.hub.list_tools().items():
            for name, tool in defs.items():
                tools[f"{vendor}.{name}"] = tool.schema
        return tools

    async def invoke(self, user: Dict[str, str], tool: str, args: Dict[str, Any]) -> Any:
        role = user.get("role", "viewer")
        self.policy.pre_check(role, tool, args)
        args = self.policy.coerce_defaults(tool, args)
        redacted_args = redact_inputs(args)
        cached = self.cache.get(tool, redacted_args)
        if cached is not None:
            return cached
        vendor, name = tool.split(".", 1)
        start = time.time()
        try:
            result = await self.hub.invoke(vendor, name, args)
            ok = True
        except Exception as e:  # pragma: no cover
            result = {"error": str(e)}
            ok = False
        latency = (time.time() - start) * 1000
        result = self.policy.project(tool, result)
        redacted_result = redact_outputs(result)
        self.cache.set(tool, redacted_args, redacted_result)
        self.audit.log(user["sub"], tool, redacted_args, redacted_result, ok, latency)
        return redacted_result

    def vendor_status(self) -> Dict[str, Any]:
        return self.hub.vendor_status()


def load_registry() -> ToolRegistry:
    return ToolRegistry()
