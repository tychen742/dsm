from otter.test_files import test_case
import numpy as np
from datascience import *

OK_FORMAT = False

name = "q2_5"
points = 6

@test_case(points=3, hidden=True)
def test_lb(lower_bound, predictions_for_eight):
    assert np.isclose(lower_bound, percentile(2.5, predictions_for_eight)) or np.isclose(lower_bound, np.percentile(predictions_for_eight, 2.5))

@test_case(points=3, hidden=True)
def test_ub(upper_bound, predictions_for_eight):
    assert np.isclose(upper_bound, percentile(97.5, predictions_for_eight)) or np.isclose(upper_bound, np.percentile(predictions_for_eight, 97.5))
