from otter.test_files import test_case
import numpy as np
from datascience import *

OK_FORMAT = False

name = "q2_1"
points = 6

@test_case(points=6, hidden=True)
def test_function(fitted_value):
    assert np.isclose(fitted_value(Table().with_columns('a', make_array(1, 2, 4), 'b', make_array(-1, 2, -15)), 'a', 'b', 3), -8.142857142857142)