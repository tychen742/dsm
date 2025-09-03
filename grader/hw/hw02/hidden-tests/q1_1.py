from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q1_1"
points = 2  

@test_case(points=1, hidden=True)
def test_q1_1_positive_numbers():
    expected = 13
    actual = sum_scores(12, 0.3, 0.6, 0.1)
    assert actual == expected, f"Expected {expected}, but got {actual}"

@test_case(points=1, hidden=True)
def test_q1_1_mixed_numbers():
    expected = -4
    actual = sum_scores(-2, 3, 5, -10)
    assert actual == expected, f"Expected {expected}, but got {actual}"


