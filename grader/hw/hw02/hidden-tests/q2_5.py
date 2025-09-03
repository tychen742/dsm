from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q2_5"
points = 4 

@test_case(points=1, hidden=True)
def test_q2_5_type(min_of_birth_years):
    assert isinstance(min_of_birth_years, (int, np.integer)), "min_of_birth_years should be an integer."

@test_case(points=3, hidden=True)
def test_q2_5_value(min_of_birth_years, president_birth_years):
    first = president_birth_years.item(0)
    sixteenth = president_birth_years.item(15)
    last = president_birth_years.item(-1)
    expected_value = min(first, sixteenth, last)
    
    assert min_of_birth_years == expected_value, f"Expected {expected_value}, but got {min_of_birth_years}."
