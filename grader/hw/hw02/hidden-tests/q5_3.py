from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q5_3"
points = 4



@test_case(points=4, hidden=True)
def test_q5_3_value(all_different):
    """
    Test that `all_different` is correctly set to either True or False based on the inventory.
    """
    expected_value = False  
    assert all_different == expected_value, f"Expected `all_different` to be {expected_value}, but got {all_different}"
