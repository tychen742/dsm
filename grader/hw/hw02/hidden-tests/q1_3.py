from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q1_3"
points = 4  

@test_case(points=2, hidden=True)
def test_q1_3_with_commas(with_commas):
    expected = "Eats, Shoots, and Leaves"
    assert with_commas == expected, f"Expected '{expected}', but got '{with_commas}'."

@test_case(points=2, hidden=True)
def test_q1_3_without_commas(without_commas):
    expected = "Eats Shoots and Leaves"
    assert without_commas == expected, f"Expected '{expected}', but got '{without_commas}'."
