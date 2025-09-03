from otter.test_files import test_case
import numpy as np
from datascience import *

OK_FORMAT = False

name = "q1_2"
points = 4

@test_case(points=2, hidden=True)
def test_function(standard_units):
    assert np.all(np.round(standard_units(make_array(5, 15, 375)), 3) == make_array(-0.736, -0.678, 1.414))

@test_case(points=2, hidden=True)
def test_function2(correlation):
    assert abs(correlation(Table().with_columns('a', np.random.normal(0, 1, 10),'b', np.random.normal(0, 1, 10)), "a", "b")) <= 1
    assert np.isclose(correlation(Table().with_columns('a', make_array(1, 2, 4), 'b', make_array(-1, 2, -15)), 'a', 'b'), -0.87779957819508425)
