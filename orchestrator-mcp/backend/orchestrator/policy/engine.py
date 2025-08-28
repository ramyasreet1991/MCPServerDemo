from fnmatch import fnmatch
from typing import Any, Dict


class PolicyEngine:
    def __init__(self, policy: Dict[str, Any]):
        self.policy = policy

    def role_for(self, role_name: str):
        roles = self.policy.get("tenancy", {}).get("roles", {})
        default = self.policy.get("tenancy", {}).get("default_role")
        return roles.get(role_name, roles.get(default, {}))

    def pre_check(self, role: str, tool: str, args: Dict[str, Any]):
        role_def = self.role_for(role)
        deny = role_def.get("deny_tools", [])
        if any(fnmatch(tool, pat) for pat in deny):
            raise PermissionError(f"Tool {tool} denied for role {role}")
        allow = role_def.get("allow_tools", [])
        if allow and not any(fnmatch(tool, pat) for pat in allow):
            raise PermissionError(f"Tool {tool} not allowed for role {role}")
        guards = self.policy.get("guards", {}).get(tool, {})
        for req in guards.get("required_args", []):
            if req not in args:
                raise ValueError(f"Missing required arg: {req}")
        for arg, allowed in guards.get("arg_allowlist", {}).items():
            if arg in args and args[arg] not in allowed:
                raise ValueError(f"Arg {arg} not allowed")

    def project(self, tool: str, result: Any) -> Any:
        return result

    def coerce_defaults(self, tool: str, args: Dict[str, Any]) -> Dict[str, Any]:
        return args
