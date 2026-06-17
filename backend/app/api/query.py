from fastapi import APIRouter

from app.schemas.query import (
    QueryRequest,
    QueryResponse
)

from app.services.query_service import QueryService

router = APIRouter(
    prefix="/api/query",
    tags=["Query"]
)


@router.post(
    "/generate",
    response_model=QueryResponse
)
def generate_query(request: QueryRequest):

    result = QueryService.generate_sql(
        request.question
    )

    return result