class QueryService:
    
    @staticmethod
    def generate_sql(question: str):
        """
        Mock SQL generator.
        AI integration will come later.
        """

        question = question.lower()

        if "customers" in question:
            sql = "SELECT * FROM customers;"

        elif "orders" in question:
            sql = "SELECT * FROM orders;"

        else:
            sql = "-- Unable to generate SQL"

        return {
            "success": True,
            "sql": sql
        }