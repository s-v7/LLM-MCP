
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal, Optional, Any

# Um "MCP" minimalista baseado em mensagens JSON Lines com id de correlação.

ProtocolVersion_C2S = Literal["mcp-min-0.1"]

class MCPEnvelope(BaseModel):
    protocol_mcp: ProtocolVersion_C2S = "mcp-min-0.1"
    kind: Literal["query", "result", "error"]
    id: str
    payload: dict

class QueryPayload(BaseModel):
    filters: dict = Field(default_factory=dict)

class CarDTO(BaseModel):
    id: int
    make: str
    model: str
    year: int
    color: str
    mileage_km: int
    price: float

class ResultPayload(BaseModel):
    items: list[CarDTO]
    total: int

class ErrorPayload(BaseModel):
    message: str
    details: Optional[Any] = None

