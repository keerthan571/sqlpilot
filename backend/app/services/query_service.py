from app.services.schema_context import SchemaContext


class QueryService:

    @staticmethod
    def generate_sql(question: str):

        schema = SchemaContext.get_schema()

        question = question.lower()

        for table_name in schema.keys():

            if table_name.lower() in question:

                return {
                    "success": True,
                    "sql": f"SELECT * FROM {table_name};"
                }

        return {
            "success": True,
            "sql": "-- No matching table found"
        }