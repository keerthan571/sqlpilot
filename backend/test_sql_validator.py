from app.services.sql_validator import SQLValidator


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


tests = [

    (
        "SQL injection",
        """
        SELECT id, name, email
        FROM customers
        WHERE name = 'Alice' OR '1'='1'
        """
    ),

    (
        "Malformed SQL injection",
        """
        SELECT id, name, email
        FROM customers
        WHERE name = 'Alice'' OR ''1''=''' '1'
        """
    )
]


print("=" * 70)

for name, sql in tests:

    valid, error = SQLValidator.validate(
        sql,
        schema
    )

    print(name)
    print("SQL:", sql.strip())
    print("VALID:", valid)
    print("ERROR:", error)
    print("-" * 70)