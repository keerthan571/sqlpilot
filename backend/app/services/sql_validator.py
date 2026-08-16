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
            table_name.lower(): table_info
            for table_name, table_info in schema.items()
        }

        # -------------------------------------------------
        # Validate every referenced table
        # -------------------------------------------------

        table_aliases = {}

        for table in statement.find_all(exp.Table):

            table_name = table.name.lower()

            if table_name not in allowed_tables:
                return (
                    False,
                    f"Table '{table.name}' does not exist."
                )

            # Store aliases so:
            # c.name -> customers.name
            alias = table.alias

            if alias:
                table_aliases[alias.lower()] = table_name

            # Also allow the actual table name
            table_aliases[table_name] = table_name

        # -------------------------------------------------
        # Build allowed columns for every table
        # -------------------------------------------------

        table_columns = {}

        for table_name, table_info in allowed_tables.items():

            table_columns[table_name] = {
                column["name"].lower()
                for column in table_info.get("columns", [])
            }

        # -------------------------------------------------
        # Validate every referenced column
        # -------------------------------------------------

        for column in statement.find_all(exp.Column):

            column_name = column.name.lower()

            # SELECT * / table.* is valid
            if column_name == "*":
                continue

            referenced_table = column.table

            # ---------------------------------------------
            # Qualified column
            #
            # Example:
            # c.name
            # orders.amount
            # ---------------------------------------------

            if referenced_table:

                table_key = referenced_table.lower()

                # Resolve alias
                actual_table = table_aliases.get(
                    table_key
                )

                if actual_table is None:
                    return (
                        False,
                        f"Table '{referenced_table}' does not exist."
                    )

                if column_name not in table_columns[actual_table]:
                    return (
                        False,
                        f"Column '{column.name}' does not exist "
                        f"in table '{actual_table}'."
                    )

            # ---------------------------------------------
            # Unqualified column
            #
            # Example:
            # SELECT name FROM customers
            # ---------------------------------------------

            else:

                found = False

                for columns in table_columns.values():

                    if column_name in columns:
                        found = True
                        break

                if not found:
                    return (
                        False,
                        f"Column '{column.name}' does not exist."
                    )

        # -------------------------------------------------
        # Detect suspicious tautological comparisons
        # -------------------------------------------------

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