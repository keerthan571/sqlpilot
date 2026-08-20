import os
import time

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

        # Try lightweight model first.
        models = [
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
        ]

        last_error = None

        for model in models:

            for attempt in range(2):

                try:

                    print(
                        f"TRYING GEMINI MODEL: "
                        f"{model} "
                        f"(attempt {attempt + 1})"
                    )

                    response = client.models.generate_content(
                        model=model,
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

                    print(
                        f"SUCCESSFUL GEMINI MODEL: {model}"
                    )

                    return sql.strip()

                except Exception as e:

                    last_error = e

                    error_text = str(e)

                    print(
                        f"GEMINI ERROR "
                        f"({model}, attempt "
                        f"{attempt + 1}): "
                        f"{error_text}"
                    )

                    # Retry only temporary server errors.
                    if "503" in error_text:

                        if attempt == 0:

                            time.sleep(2)

                            continue

                        break

                    # Don't retry authentication/quota errors.
                    raise

        # All models failed.
        if last_error:

            raise last_error

        raise RuntimeError(
            "Unable to generate SQL."
        )
        
    @staticmethod
    def explain_sql(
        question: str,
        sql: str
    ):

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

        client = genai.Client(
            api_key=api_key
        )

        prompt = f"""
        You are a helpful SQL assistant.

        Explain the following SQL query in simple,
        clear English for a beginner.

        User question:
        {question}

        Generated SQL:
        {sql}

        STRICT RULES:

        1. Explain what the query does.
        2. Mention important tables involved.
        3. Mention JOIN, WHERE, GROUP BY,
        ORDER BY, or aggregate functions only
        if they are actually present.
        4. Keep the explanation concise.
        5. Do not generate new SQL.
        6. Do not use markdown.
        7. Return only the explanation.
        """

        models = [
            "gemini-3.5-flash-lite",
            "gemini-3.1-flash-lite",
        ]

        last_error = None

        for model in models:

            for attempt in range(2):

                try:

                    print(
                        f"TRYING EXPLANATION MODEL: "
                        f"{model} "
                        f"(attempt {attempt + 1})"
                    )

                    response = client.models.generate_content(
                        model=model,
                        contents=prompt
                    )

                    if not response.text:

                        raise ValueError(
                            "Gemini returned an empty explanation."
                        )

                    explanation = response.text.strip()

                    print(
                        f"SUCCESSFUL EXPLANATION MODEL: "
                        f"{model}"
                    )

                    return explanation

                except Exception as e:

                    last_error = e
                    error_text = str(e)

                    print(
                        f"EXPLANATION ERROR "
                        f"({model}, attempt "
                        f"{attempt + 1}): "
                        f"{error_text}"
                    )

                    if "503" in error_text:

                        if attempt == 0:
                            time.sleep(2)
                            continue

                        break

                    raise

        if last_error:
            raise last_error

        raise RuntimeError(
            "Unable to generate SQL explanation."
        )