from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q3_4"
points = 4 

@test_case(points=1, hidden=True)
def test_q3_4_sum(celsius_temps_rounded):
    """
    Check if the sum of the rounded Celsius temperatures is correct.
    We allow a small tolerance to account for minor floating-point precision differences.
    """
    expected_sum = 1280677.0  # Expected sum from the dataset
    assert np.isclose(sum(celsius_temps_rounded), expected_sum, atol=1.0), \
        f"Expected sum {expected_sum}, but got {sum(celsius_temps_rounded)}"

@test_case(points=1, hidden=True)
def test_q3_4_item_check(celsius_temps_rounded):
    """
    Check if the second item in the rounded Celsius temperatures is correct.
    """
    expected_value = 31.0  # Expected value for item at index 1
    assert np.isclose(celsius_temps_rounded.item(1), expected_value), \
        f"Expected item(1) to be {expected_value}, but got {celsius_temps_rounded.item(1)}"

@test_case(points=1, hidden=True)
def test_q3_4_length(celsius_temps_rounded):
    """
    Check if the length of the rounded Celsius temperatures array is correct.
    """
    expected_length = 65000  # Expected number of elements in the dataset
    assert len(celsius_temps_rounded) == expected_length, \
        f"Expected length {expected_length}, but got {len(celsius_temps_rounded)}"

@test_case(points=1, hidden=True)
def test_q3_4_data_type(celsius_temps_rounded):
    """
    Ensure celsius_temps_rounded is a NumPy array.
    """
    assert isinstance(celsius_temps_rounded, np.ndarray), \
        "celsius_temps_rounded should be a NumPy array."