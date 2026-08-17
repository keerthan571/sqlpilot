from fastapi import APIRouter

from app.schemas.database import (
    DatabaseConnectionRequest,
    DatabaseConnectionResponse,
)
from app.services.database_service import DatabaseService
from app.services.saved_connection_service import SavedConnectionService
from app.services.database_context import DatabaseContext
from app.services.schema_context import SchemaContext

router = APIRouter(
    prefix="/api/database",
    tags=["Database"]
)

@router.get("/saved")
def get_saved_connections():
    return SavedConnectionService.list_connections()

@router.post("/reconnect/{connection_id}")
def reconnect_database(connection_id: int):
    return DatabaseService.reconnect(connection_id)

@router.post("/connect", response_model=DatabaseConnectionResponse)
def connect_database(request: DatabaseConnectionRequest):
    return DatabaseService.test_connection(request)

@router.post("/disconnect")
def disconnect_database():

    DatabaseContext.clear_engine()
    SchemaContext.clear_schema()

    return {
        "success": True,
        "message": "Database disconnected successfully."
    }

@router.get("/status")
def database_status():

    return {
        "connected": DatabaseContext.get_engine() is not None
    }
