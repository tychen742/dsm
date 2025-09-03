from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q5_1"
points = 4


@test_case(points=1, hidden=True)
def test_q5_1_type(fruits):
    """
    Test case to check if 'fruits' is a Table.
    """
    assert isinstance(fruits, Table), \
        f"Expected 'fruits' to be a Table, but got {type(fruits)}."

@test_case(points=1, hidden=True)
def test_q5_1_columns(fruits):
    """
    Test case to check if the table has the correct column labels.
    """
    expected_columns = ["fruit name", "amount"]
    assert fruits.labels == tuple(expected_columns), \
        f"Expected column names {expected_columns}, but got {fruits.labels}."

@test_case(points=2, hidden=True)
def test_q5_1_values(fruits):
    """
    Test case to check if the table contains exactly:
    - 4 apples
    - 3 oranges
    - 3 pineapples
    The order does not matter.
    """
    fruit_names = fruits.column("fruit name")
    amounts = fruits.column("amount")

    # Creating a dictionary to store expected counts
    expected_counts = {"apple": 4, "orange": 3, "pineapple": 3}

    # Creating a dictionary to store actual counts
    actual_counts = dict(zip(fruit_names, amounts))

    assert actual_counts == expected_counts, \
        f"Expected fruit amounts {expected_counts}, but got {actual_counts}."
