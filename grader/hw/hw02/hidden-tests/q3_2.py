from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q3_2"
points = 4 

@test_case(points=1, hidden=True)
def test_q3_2_length(products):
    assert isinstance(products, np.ndarray), "products should be a NumPy array."
    assert len(products) == 4, f"Expected array length of 4, but got {len(products)}."

@test_case(points=3, hidden=True)
def test_q3_2_values(products):
    numbers = make_array(42, -4224, 424224242, 250)
    expected_values = numbers * 157
    
    assert np.allclose(products, expected_values), \
        f"Expected values {expected_values}, but got {products}."