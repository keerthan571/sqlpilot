from sqlalchemy import text

from app.services.database_context import DatabaseContext


class QueryHistoryService:

    @staticmethod
    def save_query(
        question: str,
        generated_sql: str
    ):

        engine = DatabaseContext.get_engine()

        if engine is None:
            raise ValueError(
                "Database is not connected."
            )

        insert_sql = text("""
            INSERT INTO queries (
                question,
                generated_sql
            )
            VALUES (
                :question,
                :generated_sql
            )
        """)

        with engine.begin() as conn:

            conn.execute(
                insert_sql,
                {
                    "question": question,
                    "generated_sql": generated_sql
                }
            )