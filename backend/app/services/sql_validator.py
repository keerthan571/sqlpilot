from sqlglot import parse
from sqlglot import expressions as exp


class SQLValidator:

    @staticmethod
    def validate(sql: str, schema: dict):

        if not sql or not sql.strip():
            return False, "Generated SQL is empty."

        try:
            statements = parse(
                sql,
                read="postgres"
            )

        except Exception:
            return False, "Generated SQL is invalid."

        # Only one SQL statement is allowed
        if len(statements) != 1:
            return False, "Multiple SQL statements are not allowed."

        statement = statements[0]

        # Only SELECT statements are allowed
        if statement.key != "select":
            return False, "Only SELECT queries are allowed."

        # Tables available in the connected database
        allowed_tables = {
            table_name.lower()
            for table_name in schema.keys()
        }

        # Validate every referenced table
        for table in statement.find_all(exp.Table):

            table_name = table.name.lower()

            if table_name not in allowed_tables:

                return (
                    False,
                    f"Table '{table.name}' does not exist."
                )

        # Detect tautological comparisons such as:
        #
        # '1' = '1'
        # 1 = 1
        # 'abc' = 'abc'
        #
        # These can turn a WHERE condition into
        # an always-true condition.

        for comparison in statement.find_all(exp.EQ):

            left = comparison.left
            right = comparison.right

            if (
                isinstance(left, exp.Literal)
                and isinstance(right, exp.Literal)
            ):

                return (
                    False,
                    "Suspicious SQL condition detected."
                )

        return True, None