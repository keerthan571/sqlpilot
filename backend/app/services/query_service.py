from sqlalchemy import text

from app.services.schema_context import SchemaContext
from app.services.database_context import DatabaseContext


class QueryService:

    @staticmethod
    def execute(question: str):

        print("QUESTION:", question)

        schema = SchemaContext.get_schema()
        print("SCHEMA:", schema)

        engine = DatabaseContext.get_engine()
        print("ENGINE:", engine)

        sql = None

        question = question.lower()

        for table_name in schema.keys():

            print("CHECKING TABLE:", table_name)

            if table_name.lower() in question:

                sql = f"SELECT * FROM {table_name};"
                print("MATCH FOUND:", sql)
                break

        if not sql:
            print("NO MATCH FOUND")

            return {
                "success": False,
                "sql": "",
                "rows": []
            }

        with engine.connect() as conn:

            result = conn.execute(
                text(sql)
            )

            rows = [
                dict(row._mapping)
                for row in result
            ]

        return {
            "success": True,
            "sql": sql,
            "rows": rows
        }