from otter.test_files import test_case
import numpy as np
from datascience import *

OK_FORMAT = False

name = "q2_6"
points = 6

@test_case(points=2, hidden=True)
def test_value1(plover_statements):
    assert 1 in plover_statements

@test_case(points=2, hidden=True)
def test_value2(plover_statements):
    assert 2 in plover_statements
    
@test_case(points=2, hidden=True)
def test_value3(plover_statements):
    assert 3 not in plover_statements