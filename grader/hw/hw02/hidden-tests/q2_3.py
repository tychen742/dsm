from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q2_3"
points = 4 

@test_case(points=1, hidden=True)
def test_q2_3_type(index_of_last_element):
    assert isinstance(index_of_last_element, (int, np.integer)), \
        "index_of_last_element should be an integer (either Python int or NumPy int)."

@test_case(points=3, hidden=True)
def test_q2_3_value(index_of_last_element):
    expected_value = 142 - 1  
    assert index_of_last_element == expected_value, \
        f"Expected {expected_value}, but got {index_of_last_element}."

