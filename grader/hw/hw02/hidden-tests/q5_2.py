from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q5_2"
points = 4

@test_case(points=1, hidden=True)
def test_q5_2_type(inventory):
    """
    Test that `inventory` is a Table object.
    """
    assert isinstance(inventory, Table), f"Expected `inventory` to be a Table, but got {type(inventory)}"

@test_case(points=3, hidden=True)
def test_q5_2_first_value(inventory):
    """
    Dynamically test that the first item in the sorted inventory matches the expected value.
    """
    sorted_inventory = inventory.sort(0)

    expected_value = min(sorted_inventory.column(0))

    assert sorted_inventory.column(0).item(0) == expected_value, \
        f"Expected first value to be {expected_value}, but got {sorted_inventory.column(0).item(0)}"
