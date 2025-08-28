from typing import Dict, List
from pydantic import BaseModel


class Role(BaseModel):
    allow_tools: List[str] = []
    deny_tools: List[str] = []


class Tenancy(BaseModel):
    default_role: str
    roles: Dict[str, Role]


class Policy(BaseModel):
    tenancy: Tenancy
    guards: Dict[str, Dict[str, List[str]]] | None = None
