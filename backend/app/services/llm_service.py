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
                "GEMINI_API_KEY is not configured."
            )

        client = genai.Client(
            api_key=api_key
        )

        # Format schema for Gemini
        schema_text = ""

        for table, table_info in schema.items():

            schema_text += f"\nTable: {table}\n"

            for column in table_info.get(
                "columns",
                []
            ):

                schema_text += (
                    f"  - {column['name']}"
                    f" ({column['type']})\n"
                )

            primary_keys = table_info.get(
                "primary_keys",
                []
            )

            if primary_keys:

                schema_text += (
                    f"  Primary Keys: "
                    f"{', '.join(primary_keys)}\n"
                )

            foreign_keys = table_info.get(
                "foreign_keys",
                []
            )

            for foreign_key in foreign_keys:

                schema_text += (
                    "  Foreign Key: "
                    f"{foreign_key['column']} "
                    "references "
                    f"{foreign_key['references_table']}"
                    f"({foreign_key['references_column']})\n"
                )

        prompt = f"""
You are an expert PostgreSQL SQL generator
for a database assistant.

DATABASE SCHEMA:

{schema_text}

STRICT RULES:

1. Generate SQL ONLY for the user's question.
2. Use ONLY tables present in the database schema.
3. Use ONLY columns present in the database schema.
4. Respect primary-key and foreign-key relationships.
5. Generate valid PostgreSQL SQL.
6. ONLY SELECT queries are allowed.
7. NEVER generate INSERT, UPDATE, DELETE, DROP,
   ALTER, TRUNCATE, CREATE, GRANT, REVOKE,
   or any other write operation.
8. NEVER guess or substitute a different table.
9. NEVER guess or substitute a different column.
10. If the user requests a table that does not exist,
    return exactly:
    INVALID_TABLE
11. If the user requests a column that does not exist,
    return exactly:
    INVALID_COLUMN
12. If the user asks for a write/destructive operation,
    return exactly:
    UNSAFE_QUERY
13. Return ONLY SQL, INVALID_TABLE,
    INVALID_COLUMN, or UNSAFE_QUERY.
14. Do not use markdown.
15. Do not provide explanations.

USER QUESTION:

{question}
"""

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        if not response.text:
            raise ValueError(
                "Gemini returned an empty response."
            )

        sql = response.text.strip()

        # Remove markdown if Gemini returns it
        sql = sql.replace(
            "```sql",
            ""
        )

        sql = sql.replace(
            "```",
            ""
        )

        return sql.strip()