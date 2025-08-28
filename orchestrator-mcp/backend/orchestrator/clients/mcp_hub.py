from typing import Any, Dict
from dataclasses import dataclass

from ..util.logging import logger
from ..util.settings import load_yaml, settings


@dataclass
class ToolDef:
    name: str
    schema: Dict[str, Any]


class DummyVendorClient:
    def __init__(self, vendor: str):
        self.vendor = vendor
        self.tools = self._load_tools(vendor)

    def _load_tools(self, vendor: str) -> Dict[str, ToolDef]:
        # Hard coded toy implementations
        if vendor == "jira":
            return {
                "search_issues": ToolDef(
                    name="search_issues",
                    schema={
                        "type": "object",
                        "properties": {"jql": {"type": "string"}},
                        "required": ["jql"],
                    },
                )
            }
        if vendor == "outlook":
            return {
                "send_mail": ToolDef(
                    name="send_mail",
                    schema={
                        "type": "object",
                        "properties": {
                            "to": {"type": "string"},
                            "body": {"type": "string"},
                            "password": {"type": "string"},
                        },
                        "required": ["to", "body", "password"],
                    },
                )
            }
        return {
            "echo": ToolDef(
                name="echo",
                schema={
                    "type": "object",
                    "properties": {"message": {"type": "string"}},
                    "required": ["message"],
                },
            )
        }

    async def invoke(self, tool: str, args: Dict[str, Any]) -> Any:
        if tool == "search_issues":
            return {"issues": []}
        if tool == "send_mail":
            return {"status": "sent"}
        if tool == "echo":
            return {"echo": args.get("message")}
        raise ValueError("unknown tool")


class MCPHub:
    def __init__(self, config: Dict[str, Any]):
        self.clients: Dict[str, DummyVendorClient] = {}
        self.tools: Dict[str, Dict[str, ToolDef]] = {}
        for vendor in config.get("vendors", {}):
            self.add_vendor(vendor)

    def add_vendor(self, vendor: str):
        client = DummyVendorClient(vendor)
        self.clients[vendor] = client
        self.tools[vendor] = client.tools
        logger.info("Loaded vendor %s with %d tools", vendor, len(client.tools))

    def list_tools(self) -> Dict[str, Dict[str, ToolDef]]:
        return self.tools

    async def invoke(self, vendor: str, tool: str, args: Dict[str, Any]) -> Any:
        client = self.clients[vendor]
        return await client.invoke(tool, args)

    def vendor_status(self) -> Dict[str, Any]:
        return {
            name: {"tools": list(client.tools.keys()), "connected": True}
            for name, client in self.clients.items()
        }


def load_hub() -> MCPHub:
    config = load_yaml(settings.vendors_file)
    return MCPHub(config)
