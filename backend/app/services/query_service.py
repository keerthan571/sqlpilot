from sqlalchemy import text

from app.services.query_history_service import QueryHistoryService
from app.services.schema_context import SchemaContext
from app.services.database_context import DatabaseContext
from app.services.llm_service import LLMService
from app.services.sql_validator import SQLValidator


class QueryService:

    @staticmethod
    def execute(question: str):

        print("=" * 50)
        print("QUESTION:", question)

        schema = SchemaContext.get_schema()
        print("SCHEMA:", schema)

        engine = DatabaseContext.get_engine()
        print("ENGINE:", engine)

        try:

            # Generate SQL using Gemini
            sql = LLMService.generate_sql(
                question,
                schema
            )

            print("GENERATED SQL:", sql)

            # Gemini-controlled responses
            if sql == "INVALID_TABLE":

                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": (
                        "The requested table does not exist "
                        "in the connected database."
                    )
                }

            if sql == "INVALID_COLUMN":

                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": (
                        "The requested column does not exist "
                        "in the connected database."
                    )
                }

            if sql == "UNSAFE_QUERY":

                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": (
                        "Only read-only SELECT queries "
                        "are allowed."
                    )
                }

            # Backend SQL validation
            is_valid, validation_error = (
                SQLValidator.validate(
                    sql,
                    schema
                )
            )

            if not is_valid:

                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": validation_error
                }

            # Execute validated SQL
            with engine.connect() as conn:

                print("EXECUTING SQL...")

                result = conn.execute(
                    text(sql)
                )

                rows = [
                    dict(row._mapping)
                    for row in result
                ]

                print(
                    "ROWS RETURNED:",
                    len(rows)
                )

            # Save ONLY successfully executed queries
            QueryHistoryService.save_query(
                question,
                sql
            )

            print("QUERY HISTORY SAVED")

            return {
                "success": True,
                "sql": sql,
                "rows": rows,
                "error": None
            }

        except Exception as e:

            print("=" * 50)
            print("QUERY ERROR TYPE:", type(e).__name__)
            print("QUERY ERROR:", str(e))
            print("=" * 50)

            return {
                "success": False,
                "sql": "",
                "rows": [],
                "error": str(e)
            }