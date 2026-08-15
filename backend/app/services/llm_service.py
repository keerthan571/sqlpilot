import os

from dotenv import load_dotenv
from google import genai

load_dotenv()


class LLMService:

    @staticmethod
    def generate_sql(question: str, schema: dict):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured"
            )

        client = genai.Client(
            api_key=api_key
        )

        # Format database schema
        schema_text = ""

        for table_name, table_info in schema.items():

            schema_text += f"\nTable: {table_name}\n"

            for column in table_info.get("columns", []):

                schema_text += (
                    f"  Column: {column['name']} "
                    f"({column['type']})\n"
                )

            primary_keys = table_info.get(
                "primary_keys",
                []
            )

            if primary_keys:

                schema_text += (
                    "  Primary Keys: "
                    + ", ".join(primary_keys)
                    + "\n"
                )

            foreign_keys = table_info.get(
                "foreign_keys",
                []
            )

            for foreign_key in foreign_keys:

                columns = ", ".join(
                    foreign_key["column"]
                )

                referenced_columns = ", ".join(
                    foreign_key["references_column"]
                )

                schema_text += (
                    f"  Foreign Key: "
                    f"{columns} -> "
                    f"{foreign_key['references_table']}."
                    f"{referenced_columns}\n"
                )

        prompt = f"""
        You are an expert PostgreSQL SQL generator for a database assistant.

        DATABASE SCHEMA:
        {schema_text}

        STRICT RULES:

        1. Generate SQL ONLY for the user's question.
        2. Use ONLY tables present in the database schema.
        3. Use ONLY columns present in the database schema.
        4. Respect primary-key and foreign-key relationships.
        5. Generate valid PostgreSQL SQL.
        6. ONLY SELECT queries are allowed.
        7. NEVER generate INSERT, UPDATE, DELETE, DROP, ALTER,
        TRUNCATE, CREATE, GRANT, REVOKE, or any other write operation.
        8. NEVER guess or substitute a different table or column.
        9. If the user requests a table that does not exist,
        return exactly:
        INVALID_TABLE
        10. If the user requests a column that does not exist
            in the relevant table, return exactly:
            INVALID_COLUMN
        11. If the user asks for a write/destructive operation,
            return exactly:
            UNSAFE_QUERY
        12. Return ONLY SQL, INVALID_TABLE, INVALID_COLUMN,
            or UNSAFE_QUERY.
        13. Do not use markdown.
        14. Do not provide explanations.

        USER QUESTION:
        {question}
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        # Gemini may return no text for blocked/unsafe prompts.
        if not response.text:
            return "UNSAFE_QUERY"

        sql = response.text.strip()

        # Remove markdown fences if Gemini returns them
        if sql.startswith("```sql"):
            sql = sql[6:]

        elif sql.startswith("```"):
            sql = sql[3:]

        if sql.endswith("```"):
            sql = sql[:-3]

        return sql.strip()