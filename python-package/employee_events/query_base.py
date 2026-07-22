from .sql_execution import QueryMixin

class QueryBase(QueryMixin):

    name = ""

    def names(self):
        return []

    def event_counts(self, id):
        return self.pandas_query(f"""
            SELECT event_date,
                   SUM(positive_events) AS positive_events,
                   SUM(negative_events) AS negative_events
            FROM {self.name}
            JOIN employee_events
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
            GROUP BY event_date
            ORDER BY event_date
        """)

    def notes(self, id):
        return self.pandas_query(f"""
            SELECT note_date, note
            FROM {self.name}
            JOIN notes
                USING({self.name}_id)
            WHERE {self.name}.{self.name}_id = {id}
        """)
