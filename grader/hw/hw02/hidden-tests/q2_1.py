from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q2_1"
points = 4


@test_case(points=4, hidden=True)
def test_q2_1_value(third_element):
    expected_value = -6
    assert third_element == expected_value, f"Expected {expected_value}, but got {third_element}."
