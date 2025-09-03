from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q4_2"
points = 4

@test_case(points=1, hidden=True)
def test_q4_2_type(biggest_decrease):
    """
    Check if biggest_decrease is an int or float.
    """
    assert isinstance(biggest_decrease, (int, float, np.integer)), \
        f"Expected biggest_decrease to be an int or float, but got {type(biggest_decrease)}."

@test_case(points=3, hidden=True)
def test_q4_2_value(biggest_decrease, waiting_times):
    """
    Dynamically checking if biggest_decrease matches the largest decrease in the dataset.
    """
    import numpy as np

    differences = np.diff(waiting_times)
    expected_value = abs(differences.min())  

    assert biggest_decrease == expected_value, \
        f"Expected biggest_decrease to be {expected_value}, but got {biggest_decrease}."
