from otter.test_files import test_case
import numpy as np
from datascience import *

OK_FORMAT = False

name = "q1_5"
points = 8

@test_case(points=4, hidden=True)
def test_le(lower_end, resampled_slopes):
    assert np.isclose(lower_end, percentile(2.5, resampled_slopes)) or np.isclose(lower_end, np.percentile(resampled_slopes, 2.5))

@test_case(points=4, hidden=True)
def test_ue(upper_end, resampled_slopes):
    assert np.isclose(upper_end, percentile(97.5, resampled_slopes)) or np.isclose(upper_end, np.percentile(resampled_slopes, 97.5))
