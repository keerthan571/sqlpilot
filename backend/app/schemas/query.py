from typing import Any

from pydantic import BaseModel


class QueryRequest(BaseModel):

    question: str


class QueryResponse(BaseModel):

    success: bool
    sql: str
    explanation: str | None = None
    rows: list[dict[str, Any]] = []
    error: str | None = None