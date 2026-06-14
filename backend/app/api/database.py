from fastapi import APIRouter

from app.schemas.database import (
    DatabaseConnectionRequest,
    DatabaseConnectionResponse,
)
from app.services.database_service import DatabaseService

router = APIRouter(
    prefix="/api/database",
    tags=["Database"]
)


@router.post("/connect", response_model=DatabaseConnectionResponse)
def connect_database(request: DatabaseConnectionRequest):
    return DatabaseService.test_connection(request)