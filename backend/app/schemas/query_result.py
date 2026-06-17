from pydantic import BaseModel
from typing import Any


class QueryExecutionResponse(BaseModel):
    success: bool
    sql: str
    rows: list[dict[str, Any]]
    error: str | None = None