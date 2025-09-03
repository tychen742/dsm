from otter.test_files import test_case
import numpy as np
from datascience import *

OK_FORMAT = False

name = "q1_3"
points = 8

@test_case(points=8, hidden=True)
def test_function(fit_line):
    assert np.all(np.round(fit_line(Table().with_columns('a', make_array(1, 2, 4), 'b', make_array(-1, 2, -15)), 'a', 'b'), 3) == make_array(-5.214, 7.5))
