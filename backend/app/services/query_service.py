from sqlalchemy import text

from app.services.schema_context import SchemaContext
from app.services.database_context import DatabaseContext
from app.services.llm_service import LLMService


class QueryService:

    @staticmethod
    def execute(question: str):

        print("=" * 50)
        print("QUESTION:", question)

        schema = SchemaContext.get_schema()
        print("SCHEMA:", schema)

        engine = DatabaseContext.get_engine()
        print("ENGINE:", engine)

        # Generate SQL using Gemini
        sql = LLMService.generate_sql(
            question,
            schema
        )

        print("GENERATED SQL:", sql)

        # Safety check
        clean_sql = sql.strip().lower()

        if not clean_sql.startswith("select"):

            return {
                "success": False,
                "sql": sql,
                "rows": [],
                "error": "Only SELECT queries are allowed"
            }

        try:

            with engine.connect() as conn:

                print("EXECUTING SQL...")

                result = conn.execute(
                    text(sql)
                )

                rows = [
                    dict(row._mapping)
                    for row in result
                ]

                print("ROWS RETURNED:", len(rows))

            return {
                "success": True,
                "sql": sql,
                "rows": rows,
                "error": None
            }

        except Exception as e:

            print("SQL ERROR:")
            print(str(e))

            # Return exact error to frontend
            return {
                "success": False,
                "sql": sql,
                "rows": [],
                "error": str(e)
            }