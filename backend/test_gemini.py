from app.services.llm_service import LLMService

schema = {
    "customers": [
        "id",
        "name",
        "email"
    ]
}

sql = LLMService.generate_sql(
    "show all customers",
    schema
)

print(sql)