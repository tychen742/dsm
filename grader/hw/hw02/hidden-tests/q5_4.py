from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q5_4"
points = 5

@test_case(points=1, hidden=True)
def test_q5_4_type(sales):
    """
    Test that `sales` is a Table.
    """
    assert hasattr(sales, 'num_rows'), "Expected `sales` to be a Table."

@test_case(points=1, hidden=True)
def test_q5_4_columns(sales):
    """
    Test that `sales` contains the correct column names.
    """
    expected_columns = {'box ID', 'fruit name', 'count sold', 'price per fruit ($)'}
    assert set(sales.labels) == expected_columns, f"Expected columns {expected_columns}, but got {set(sales.labels)}."

@test_case(points=1, hidden=True)
def test_q5_4_fruit_names(sales):
    """
    Test that `sales` contains expected fruit names.
    """
    expected_fruits = {'apple', 'strawberry', 'peach', 'orange', 'kiwi', 'grape'}
    assert set(sales.column('fruit name')) & expected_fruits, "Expected some valid fruit names in sales data."

@test_case(points=2, hidden=True)
def test_q5_4_box_id(sales):
    """
    Test that the third lowest box ID is present in sales.
    """
    sorted_box_ids = sorted(sales.column('box ID'))
    expected_third_lowest = 43566  
    assert sorted_box_ids[2] == expected_third_lowest, f"Expected third lowest box ID to be {expected_third_lowest}, but got {sorted_box_ids[2]}."

