from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

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

        # Get currently active saved connection
        connection_id = DatabaseContext.get_connection_id()
        print("ACTIVE CONNECTION ID:", connection_id)

        # -----------------------------------------
        # Database connection check
        # -----------------------------------------

        if engine is None:
            return {
                "success": False,
                "sql": "",
                "rows": [],
                "error": "Database is not connected. Please connect a database first."
            }

        if connection_id is None:
            return {
                "success": False,
                "sql": "",
                "rows": [],
                "error": "No active database connection found."
            }

        try:

            # -----------------------------------------
            # Generate SQL
            # -----------------------------------------

            sql = LLMService.generate_sql(
                question,
                schema
            )

            print("GENERATED SQL:", sql)

            # -----------------------------------------
            # Gemini-controlled responses
            # -----------------------------------------

            if sql == "INVALID_TABLE":
                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": "The requested table does not exist in the connected database."
                }

            if sql == "INVALID_COLUMN":
                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": "The requested column does not exist in the connected database."
                }

            if sql == "UNSAFE_QUERY":
                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": "Only read-only SELECT queries are allowed."
                }

            # -----------------------------------------
            # SQL validation
            # -----------------------------------------

            is_valid, validation_error = SQLValidator.validate(
                sql,
                schema
            )

            if not is_valid:
                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": validation_error
                }

            # -----------------------------------------
            # Execute SQL
            # -----------------------------------------

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

            # -----------------------------------------
            # Generate SQL explanation
            # -----------------------------------------

            explanation = None

            try:

                explanation = LLMService.explain_sql(
                    question,
                    sql
                )

                print(
                    "SQL EXPLANATION:",
                    explanation
                )

            except Exception as explanation_error:

                print(
                    "EXPLANATION ERROR:",
                    str(explanation_error)
                )
            
            # -----------------------------------------
            # Save history
            # -----------------------------------------

            try:

                QueryHistoryService.save_query(
                    connection_id,
                    question,
                    sql
                )

                print(
                    "QUERY HISTORY SAVED FOR CONNECTION:",
                    connection_id
                )

            except Exception as history_error:

                print(
                    "HISTORY SAVE ERROR:",
                    str(history_error)
                )

            # -----------------------------------------
            # Success
            # -----------------------------------------

            return {
                "success": True,
                "sql": sql,
                "explanation": explanation,
                "rows": rows,
                "error": None
            }

        except Exception as e:

            print("=" * 50)
            print(
                "QUERY ERROR TYPE:",
                type(e).__name__
            )
            print(
                "QUERY ERROR:",
                str(e)
            )
            print("=" * 50)

            error_text = str(e).lower()

            # -----------------------------------------
            # Gemini quota
            # -----------------------------------------

            if (
                "429" in error_text
                or "resource_exhausted" in error_text
                or "quota" in error_text
            ):
                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": "Gemini API quota has been exceeded. Please try again later."
                }

            # -----------------------------------------
            # Gemini model unavailable
            # -----------------------------------------

            if (
                "404" in error_text
                and "model" in error_text
            ):
                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": "The configured Gemini model is currently unavailable."
                }

            # -----------------------------------------
            # Gemini API key
            # -----------------------------------------

            if (
                "api key" in error_text
                or "api_key" in error_text
                or "no api key was provided" in error_text
            ):
                return {
                    "success": False,
                    "sql": "",
                    "rows": [],
                    "error": "Gemini API key is missing or invalid."
                }

            # -----------------------------------------
            # Database / SQLAlchemy error
            # -----------------------------------------

            if isinstance(e, SQLAlchemyError):
                return {
                    "success": True,
                    "sql": sql,
                    "explanation": explanation,
                    "rows": rows,
                    "error": None
                }

            # -----------------------------------------
            # Unknown error
            # -----------------------------------------

            return {
                "success": True,
                "sql": sql,
                "explanation": explanation,
                "rows": rows,
                "error": None
            }