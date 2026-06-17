from fastapi import APIRouter

from app.schemas.query import QueryRequest
from app.schemas.query_result import QueryExecutionResponse

from app.services.query_service import QueryService

router = APIRouter(
    prefix="/api/query",
    tags=["Query"]
)


@router.post(
    "/generate",
    response_model=QueryExecutionResponse
)
def generate_query(
    request: QueryRequest
):

    return QueryService.execute(
        request.question
    )