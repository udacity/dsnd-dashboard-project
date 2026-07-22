from .query_base import QueryBase
from .sql_execution import query

class Team(QueryBase):

    name = "team"

    @query
    def names(self):
        return """
            SELECT team_name, team_id
            FROM team
        """

    @query
    def username(self, id):
        return f"""
            SELECT team_name
            FROM team
            WHERE team_id = {id}
        """

    def model_data(self, id):
        return self.pandas_query(f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """)
