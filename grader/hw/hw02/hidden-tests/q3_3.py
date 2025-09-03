from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q3_3"
points = 4 

@test_case(points=1, hidden=True)
def test_q3_3_length(correct_products):
    assert isinstance(correct_products, np.ndarray), "correct_products should be a NumPy array."
    assert len(correct_products) == 4, f"Expected array length of 4, but got {len(correct_products)}."

@test_case(points=3, hidden=True)
def test_q3_3_values(correct_products):
    numbers = make_array(42, -4224, 424224242, 250)
    expected_values = numbers * 1577  # Updated multiplication factor

    assert np.allclose(correct_products, expected_values), \
        f"Expected values {expected_values}, but got {correct_products}."