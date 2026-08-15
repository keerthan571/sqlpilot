from app.services.database_context import DatabaseContext
from app.services.query_history_service import QueryHistoryService
from app.services.database_service import DatabaseService


config = type(
    "DatabaseConfig",
    (),
    {
        "db_type": "postgresql",
        "host": "localhost",
        "port": 5432,
        "username": "postgres",
        "password": "panjurli@123",
        "database": "sqlpilot_demo"
    }
)()


DatabaseService.test_connection(config)

QueryHistoryService.save_query(
    "test query history",
    "SELECT * FROM customers"
)

print("QUERY HISTORY TEST PASSED")