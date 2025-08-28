from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import Any, Dict

from ..server import load_registry

app = FastAPI()
registry = load_registry()


class InvokeRequest(BaseModel):
    tool: str
    args: Dict[str, Any] = {}


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/tools")
async def tools():
    return registry.list_tools()


@app.get("/vendors")
async def vendors():
    return registry.vendor_status()


@app.post("/invoke")
async def invoke(
    req: InvokeRequest,
    authorization: str | None = Header(default=None),
    x_user: str | None = Header(default="anon"),
    x_role: str | None = Header(default="viewer"),
):
    user = {"sub": x_user, "role": x_role}
    try:
        result = await registry.invoke(user, req.tool, req.args)
        return {"result": result}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
