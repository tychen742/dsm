from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q2_2"
points = 4  

@test_case(points=1, hidden=True)
def test_q2_2_1(elements_of_some_numbers):
    """
    Test if the third English name is 'third'.
    """
    assert elements_of_some_numbers.column(0).item(2) == "third", \
        f"Expected 'third', but got {elements_of_some_numbers.column(0).item(2)}"

@test_case(points=1, hidden=True)
def test_q2_2_2(elements_of_some_numbers):
    """
    Test if the fourth English name is 'fourth'.
    """
    assert elements_of_some_numbers.column(0).item(3) == "fourth", \
        f"Expected 'fourth', but got {elements_of_some_numbers.column(0).item(3)}"

@test_case(points=1, hidden=True)
def test_q2_2_3(elements_of_some_numbers):
    """
    Test if the first index is 0.
    """
    assert elements_of_some_numbers.column(1).item(0) == 0, \
        f"Expected 0, but got {elements_of_some_numbers.column(1).item(0)}"

@test_case(points=1, hidden=True)
def test_q2_2_4(elements_of_some_numbers):
    """
    Test if the fourth index is 3.
    """
    assert elements_of_some_numbers.column(1).item(3) == 3, \
        f"Expected 3, but got {elements_of_some_numbers.column(1).item(3)}"
