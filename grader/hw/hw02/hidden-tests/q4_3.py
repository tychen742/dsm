from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q4_3"
points = 4

@test_case(points=1, hidden=True)
def test_q4_3_length(first_nine_waiting_times):
    """
    Check if the first_nine_waiting_times array has length 9.
    """
    assert len(first_nine_waiting_times) == 9, \
        f"Expected length of 9, but got {len(first_nine_waiting_times)}"

@test_case(points=3, hidden=True)
def test_q4_3_total_waiting_time(total_waiting_time_until_tenth, faithful_with_eruption_nums):
    """
    Dynamically check if the total waiting time until the tenth eruption matches the dataset.
    """
    first_nine_waiting_times = faithful_with_eruption_nums.column('waiting')[:9]

    expected_value = sum(first_nine_waiting_times)

    assert total_waiting_time_until_tenth == expected_value, \
        f"Expected {expected_value}, but got {total_waiting_time_until_tenth}"

    