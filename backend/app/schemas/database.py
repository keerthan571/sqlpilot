from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class DatabaseConnectionRequest(BaseModel):
    db_type: Literal["postgresql", "mysql", "sqlite"]
    host: str
    port: int
    username: str
    password: str
    database: str


class DatabaseConnectionResponse(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True
    )

    success: bool
    message: str
    database_type: str

    schema_: dict | None = Field(
        default=None,
        alias="schema"
    )