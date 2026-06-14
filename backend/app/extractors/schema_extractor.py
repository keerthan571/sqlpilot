from sqlalchemy import inspect


class SchemaExtractor:

    @staticmethod
    def extract(engine):

        inspector = inspect(engine)

        schema = {}

        for table in inspector.get_table_names():

            schema[table] = {
                "columns": [],
                "primary_keys": [],
                "foreign_keys": []
            }

            # Columns
            for column in inspector.get_columns(table):
                schema[table]["columns"].append({
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                    "default": str(column.get("default"))
                })

            # Primary Keys
            pk = inspector.get_pk_constraint(table)

            schema[table]["primary_keys"] = pk.get(
                "constrained_columns",
                []
            )

            # Foreign Keys
            for fk in inspector.get_foreign_keys(table):

                schema[table]["foreign_keys"].append({

                    "column": fk.get("constrained_columns"),

                    "references_table": fk.get("referred_table"),

                    "references_column": fk.get("referred_columns")
                })

        return schema