from fastapi import APIRouter

from app.schemas.database import DatabaseConnectionRequest
from app.services.database_service import DatabaseService

router = APIRouter(prefix="/api/database", tags=["Database"])


@router.post("/connect")
def connect_database(request: DatabaseConnectionRequest):

    success, message = DatabaseService.test_connection(request)

    return {
        "success": success,
        "message": message,
    }