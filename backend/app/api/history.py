from fastapi import APIRouter

from app.services.database_context import DatabaseContext
from app.schemas.query_history import QueryHistoryResponse

from sqlalchemy import text


router = APIRouter(
    prefix="/api/history",
    tags=["Query History"]
)


@router.get(
    "",
    response_model=list[QueryHistoryResponse]
)
def get_query_history():

    engine = DatabaseContext.get_engine()

    if engine is None:
        return []

    query = text("""
        SELECT
            id,
            question,
            generated_sql,
            created_at
        FROM queries
        ORDER BY created_at DESC
    """)

    with engine.connect() as conn:

        result = conn.execute(query)

        rows = [
            dict(row._mapping)
            for row in result
        ]

    return rows