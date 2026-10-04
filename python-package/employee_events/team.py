# Import the QueryBase class
from .query_base import QueryBase

# Import dependencies for sql execution
from .sql_execution import query


# Create a subclass of QueryBase
# called  `Team`
class Team(QueryBase):

    # Set the class attribute `name`
    # to the string "team"
    name = "team"

    # Define a `names` method
    # that receives no arguments
    # This method should return
    # a list of tuples from an sql execution
    @query
    def names(self):

        # Query 5
        # Write an SQL query that selects
        # the team_name and team_id columns
        # from the team table for all teams
        # in the database
        return """
            SELECT team_name, team_id
            FROM team
        """

    # Define a `username` method
    # that receives an ID argument
    # This method should return
    # a list of tuples from an sql execution
    @query
    def username(self, id):

        # Query 6
        # Write an SQL query
        # that selects the team_name column
        # Use f-string formatting and a WHERE filter
        # to only return the team name related to
        # the ID argument
        return f"""
            SELECT team_name
            FROM team
            WHERE team_id = {id}
        """

    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
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
