import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class LLMService:

    @staticmethod
    def generate_sql(question: str, schema: dict):

        genai.configure(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

        # Format schema nicely
        schema_text = ""

        for table, columns in schema.items():

            schema_text += f"\nTable: {table}\n"

            for column in columns:
                schema_text += f"  - {column}\n"

        prompt = f"""
You are an expert PostgreSQL SQL generator.

Database Schema:

{schema_text}

Rules:
1. Return ONLY SQL.
2. Do NOT use markdown.
3. Do NOT explain anything.
4. Use only tables and columns from the schema.
5. Generate a valid PostgreSQL query.

Question:
{question}
"""

        response = model.generate_content(prompt)

        sql = response.text.strip()

        # Remove markdown if Gemini still returns it
        sql = sql.replace("```sql", "")
        sql = sql.replace("```", "")
        sql = sql.strip()

        return sql