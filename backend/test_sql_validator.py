from app.services.sql_validator import SQLValidator


schema = {
    "customers": {
        "columns": [
            {"name": "id"},
            {"name": "name"},
            {"name": "email"}
        ]
    },
    "orders": {
        "columns": [
            {"name": "id"},
            {"name": "customer_id"},
            {"name": "amount"}
        ]
    }
}


tests = [
    (
        "Normal SELECT",
        "SELECT id, name, email FROM customers"
    ),

    (
        "JOIN",
        """
        SELECT c.name, SUM(o.amount)
        FROM customers c
        JOIN orders o
        ON c.id = o.customer_id
        GROUP BY c.name
        """
    ),

    (
        "Invalid table",
        "SELECT * FROM employees"
    ),

    (
        "DELETE",
        "DELETE FROM customers"
    ),

    (
        "Multiple statements",
        "SELECT * FROM customers; DELETE FROM customers"
    ),

    (
        "SQL injection",
        """
        SELECT id, name, email
        FROM customers
        WHERE name = 'Alice' OR '1'='1'
        """
    )
]


for test_name, sql in tests:

    valid, error = SQLValidator.validate(
        sql,
        schema
    )

    print("=" * 60)
    print(test_name)
    print("SQL:", sql.strip())
    print("VALID:", valid)
    print("ERROR:", error)