import pytest
from pathlib import Path

# Using pathlib create a project_root
# variable set to the absolute path
# for the root of this project
project_root = Path(__file__).resolve().parent.parent


# apply the pytest fixture decorator
# to a `db_path` function
@pytest.fixture
def db_path():

    # Using the `project_root` variable
    # return a pathlib object for the `employee_events.db` file
    return project_root / 'python-package' / 'employee_events' / 'employee_events.db'


# Define a function called
# `test_db_exists`
# This function should receive an argument
# with the same name as the function
# the creates the "fixture" for
# the database's filepath
def test_db_exists(db_path):

    # using the pathlib `.is_file` method
    # assert that the sqlite database file exists
    # at the location passed to the test_db_exists function
    assert db_path.is_file()


@pytest.fixture
def db_conn(db_path):
    from sqlite3 import connect
    return connect(db_path)


@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    return [x[0] for x in name_tuples]


# Define a test function called
# `test_employee_table_exists`
# This function should receive the `table_names`
# fixture as an argument
def test_employee_table_exists(table_names):

    # Assert that the string 'employee'
    # is in the table_names list
    assert 'employee' in table_names


# Define a test function called
# `test_team_table_exists`
# This function should receive the `table_names`
# fixture as an argument
def test_team_table_exists(table_names):

    # Assert that the string 'team'
    # is in the table_names list
    assert 'team' in table_names


# Define a test function called
# `test_employee_events_table_exists`
# This function should receive the `table_names`
# fixture as an argument
def test_employee_events_table_exists(table_names):

    # Assert that the string 'employee_events'
    # is in the table_names list
    assert 'employee_events' in table_names
