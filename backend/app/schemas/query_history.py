from pydantic import BaseModel
from datetime import datetime


class QueryHistoryResponse(BaseModel):
    id: int
    question: str
    generated_sql: str
    created_at: datetime