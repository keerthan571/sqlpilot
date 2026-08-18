from fastapi import APIRouter
from sqlalchemy import text

from app.services.database_context import DatabaseContext
from app.services.query_history_service import QueryHistoryService
from app.schemas.query_history import QueryHistoryResponse


router = APIRouter(
    prefix="/api/history",
    tags=["Query History"]
)


@router.get(
    "",
    response_model=list[QueryHistoryResponse]
)
def get_query_history():

    # Get currently active database connection
    connection_id = DatabaseContext.get_connection_id()

    # No database is currently active
    if connection_id is None:
        return []

    # Ensure SQLPilot's internal history table exists
    QueryHistoryService.initialize()

    # Use SQLPilot's internal history database
    engine = QueryHistoryService._get_engine()

    # Return history only for the active connection
    query = text("""
        SELECT
            id,
            question,
            generated_sql,
            created_at
        FROM queries
        WHERE connection_id = :connection_id
        ORDER BY created_at DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(
            query,
            {
                "connection_id": connection_id
            }
        )

        rows = [
            dict(row._mapping)
            for row in result
        ]

    return rows