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

@router.delete("/saved/{connection_id}")
def delete_saved_connection(connection_id: int):

    deleted = SavedConnectionService.delete(connection_id)

    if not deleted:
        return {
            "success": False,
            "message": "Saved connection not found."
        }

    return {
        "success": True,
        "message": "Saved connection deleted successfully."
    }

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

    engine = DatabaseContext.get_engine()
    connection_id = DatabaseContext.get_connection_id()

    if engine is None or connection_id is None:
        return {
            "connected": False,
            "connection_id": None,
            "database_type": None,
            "database_name": None
        }

    saved_connection = SavedConnectionService.get_connection(
        connection_id
    )

    if not saved_connection:
        return {
            "connected": False,
            "connection_id": None,
            "database_type": None,
            "database_name": None
        }

    return {
        "connected": True,
        "connection_id": connection_id,
        "database_type": saved_connection["db_type"],
        "database_name": saved_connection["database_name"]
    }
