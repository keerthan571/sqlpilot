from typing import Literal
from pydantic import BaseModel


class DatabaseConnectionRequest(BaseModel):
    db_type: Literal["postgresql", "mysql", "sqlite"]
    host: str
    port: int
    username: str
    password: str
    database: str


class DatabaseConnectionResponse(BaseModel):
    success: bool
    message: str
    database_type: str
    schema: dict | None = None