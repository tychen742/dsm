from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q2_4"
points = 4 

@test_case(points=1, hidden=True)
def test_q2_4_type(most_recent_birth_year):
    assert isinstance(most_recent_birth_year, (int, np.integer)), "most_recent_birth_year should be an integer."

@test_case(points=3, hidden=True)
def test_q2_4_value(most_recent_birth_year, president_birth_years):
    expected_value = np.max(president_birth_years)  
    assert most_recent_birth_year == expected_value, f"Expected {expected_value}, but got {most_recent_birth_year}."
