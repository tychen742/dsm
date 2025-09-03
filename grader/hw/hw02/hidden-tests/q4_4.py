from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q4_4"
points = 4

@test_case(points=1, hidden=True)
def test_q4_4_type(average_error):
    """
    Test case to check if average_error is of type int or float.
    """
    assert isinstance(average_error, (int, float, np.integer)), \
        f"Expected average_error to be an int or float, but got {type(average_error)}."


@test_case(points=3, hidden=True)
def test_q4_4_exact_value(average_error, waiting_times):
    """
    Dynamically check if average_error matches the computed value from the dataset.
    """

    differences = np.diff(waiting_times)

    expected_value = np.mean(np.abs(differences))

    assert np.isclose(average_error, expected_value, atol=0.1), \
        f"Expected average_error to be approximately {expected_value:.2f}, but got {average_error:.2f}."
