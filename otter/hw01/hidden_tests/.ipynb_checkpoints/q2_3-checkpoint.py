from otter.test_files import test_case
import numpy as np
from datascience import *

OK_FORMAT = False

name = "q2_3"
points = 6

@test_case(points=6, hidden=True)
def test_function(compute_resampled_line):
    np.random.seed(123)
    assert np.all(np.round(compute_resampled_line(Table().with_columns('a', make_array(1, 2, 4), 'b', make_array(-1, 2, -15)), 'a', 'b'), 2) == make_array(-8.5, 19))