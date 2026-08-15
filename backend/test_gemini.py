from app.services.llm_service import LLMService


schema = {
    "customers": {
        "columns": [
            {
                "name": "id",
                "type": "INTEGER"
            },
            {
                "name": "name",
                "type": "VARCHAR(100)"
            },
            {
                "name": "email",
                "type": "VARCHAR(100)"
            }
        ],
        "primary_keys": ["id"],
        "foreign_keys": []
    },
    "orders": {
        "columns": [
            {
                "name": "id",
                "type": "INTEGER"
            },
            {
                "name": "customer_id",
                "type": "INTEGER"
            },
            {
                "name": "amount",
                "type": "NUMERIC(10, 2)"
            }
        ],
        "primary_keys": ["id"],
        "foreign_keys": [
            {
                "column": ["customer_id"],
                "references_table": "customers",
                "references_column": ["id"]
            }
        ]
    }
}


sql = LLMService.generate_sql(
    "show all customers",
    schema
)


print("GENERATED SQL:")
print(sql)