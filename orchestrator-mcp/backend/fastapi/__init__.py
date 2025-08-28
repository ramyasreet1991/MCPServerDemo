import inspect
import asyncio
from types import SimpleNamespace
from typing import Callable, Dict, Any


class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


def Header(default=None):
    return default


class FastAPI:
    def __init__(self):
        self.routes: Dict[tuple[str, str], Callable] = {}

    def get(self, path: str):
        def decorator(func: Callable):
            self.routes[("GET", path)] = func
            return func
        return decorator

    def post(self, path: str):
        def decorator(func: Callable):
            self.routes[("POST", path)] = func
            return func
        return decorator

    def __call__(self, method: str, path: str, json: dict | None = None, headers: dict | None = None):
        func = self.routes.get((method, path))
        if not func:
            raise HTTPException(404, "Not found")
        params: Dict[str, Any] = {}
        if json:
            # assume first param is request body
            first = list(inspect.signature(func).parameters)[0]
            params[first] = SimpleNamespace(**json)
        headers = headers or {}
        for k, v in headers.items():
            params[k.replace("-", "_").lower()] = v
        if inspect.iscoroutinefunction(func):
            return asyncio.get_event_loop().run_until_complete(func(**params))
        return func(**params)


class Response:
    def __init__(self, status_code: int, data: Any):
        self.status_code = status_code
        self.data = data

    def json(self):
        return self.data


class TestClient:
    def __init__(self, app: FastAPI):
        self.app = app

    def get(self, path: str, headers: dict | None = None):
        try:
            data = self.app("GET", path, headers=headers)
            return Response(200, data)
        except HTTPException as e:
            return Response(e.status_code, {"detail": e.detail})

    def post(self, path: str, json: dict | None = None, headers: dict | None = None):
        try:
            data = self.app("POST", path, json=json, headers=headers)
            return Response(200, data)
        except HTTPException as e:
            return Response(e.status_code, {"detail": e.detail})
