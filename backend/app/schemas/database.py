from pydantic import BaseModel


class DatabaseConnectionRequest(BaseModel):
    db_type: str
    host: str
    port: int
    username: str
    password: str
    database: str