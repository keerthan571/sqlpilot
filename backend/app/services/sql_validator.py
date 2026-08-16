import re

from sqlglot import parse
from sqlglot import expressions as exp


class SQLValidator:

    @staticmethod
    def validate(sql: str, schema: dict):

        if not sql or not sql.strip():
            return False, "Generated SQL is empty."

        normalized_sql = sql.strip()

        # ---------------------------------------------------------
        # 1. Block multiple SQL statements
        # ---------------------------------------------------------

        try:

            statements = parse(
                normalized_sql,
                read="postgres"
            )

        except Exception:

            return False, "Generated SQL is invalid."

        if len(statements) != 1:

            return (
                False,
                "Multiple SQL statements are not allowed."
            )

        statement = statements[0]

        # ---------------------------------------------------------
        # 2. Only SELECT statements
        # ---------------------------------------------------------

        if statement.key != "select":

            return (
                False,
                "Only SELECT queries are allowed."
            )

        # ---------------------------------------------------------
        # 3. Validate referenced tables
        # ---------------------------------------------------------

        allowed_tables = {
            table_name.lower()
            for table_name in schema.keys()
        }

        for table in statement.find_all(exp.Table):

            table_name = table.name.lower()

            if table_name not in allowed_tables:

                return (
                    False,
                    f"Table '{table.name}' does not exist."
                )

        # ---------------------------------------------------------
        # 4. Validate referenced columns
        # ---------------------------------------------------------

        allowed_columns = {
            table_name.lower(): {
                column["name"].lower()
                for column in table_info.get(
                    "columns",
                    []
                )
            }
            for table_name, table_info in schema.items()
        }

        for column in statement.find_all(exp.Column):

            column_name = column.name.lower()

            # Ignore wildcard
            if column_name == "*":
                continue

            # Qualified column: table.column
            if column.table:

                table_name = column.table.lower()

                if table_name not in allowed_tables:
                    continue

                if (
                    column_name
                    not in allowed_columns.get(
                        table_name,
                        set()
                    )
                ):

                    return (
                        False,
                        f"Column '{column.name}' does not exist."
                    )

            else:

                # Unqualified column.
                # It must exist in at least one allowed table.
                exists = any(
                    column_name in columns
                    for columns in allowed_columns.values()
                )

                if not exists:

                    return (
                        False,
                        f"Column '{column.name}' does not exist."
                    )

        # ---------------------------------------------------------
        # 5. Detect suspicious literal comparisons
        # ---------------------------------------------------------

        literal_comparison_pattern = re.compile(
            r"""
            (?:
                '(?:''|[^'])*'
                |
                \b\d+(?:\.\d+)?\b
            )
            \s*=\s*
            (?:
                '(?:''|[^'])*'
                |
                \b\d+(?:\.\d+)?\b
            )
            """,
            re.IGNORECASE | re.VERBOSE
        )

        if literal_comparison_pattern.search(
            normalized_sql
        ):

            return (
                False,
                "Suspicious SQL condition detected."
            )

        # ---------------------------------------------------------
        # 6. Detect boolean tautology patterns
        # ---------------------------------------------------------

        tautology_pattern = re.compile(
            r"""
            \bOR\b
            \s+
            (?:
                '(?:''|[^'])*'
                |
                \b\d+(?:\.\d+)?\b
            )
            \s*=\s*
            (?:
                '(?:''|[^'])*'
                |
                \b\d+(?:\.\d+)?\b
            )
            """,
            re.IGNORECASE | re.VERBOSE
        )

        if tautology_pattern.search(
            normalized_sql
        ):

            return (
                False,
                "Suspicious SQL condition detected."
            )

        # ---------------------------------------------------------
        # 7. Detect SQL comments
        # ---------------------------------------------------------

        if "--" in normalized_sql:
            return (
                False,
                "SQL comments are not allowed."
            )

        if "/*" in normalized_sql or "*/" in normalized_sql:
            return (
                False,
                "SQL comments are not allowed."
            )

        # ---------------------------------------------------------
        # 8. AST-level literal comparison check
        # ---------------------------------------------------------

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