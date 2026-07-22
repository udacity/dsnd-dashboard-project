from .query_base import QueryBase
from .sql_execution import query

class Employee(QueryBase):

    name = "employee"

    @query
    def names(self):
        return """
            SELECT first_name || ' ' || last_name, employee_id
            FROM employee
        """

    @query
    def username(self, id):
        return f"""
            SELECT first_name || ' ' || last_name
            FROM employee
            WHERE employee_id = {id}
        """

    def model_data(self, id):
        return self.pandas_query(f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                """)
