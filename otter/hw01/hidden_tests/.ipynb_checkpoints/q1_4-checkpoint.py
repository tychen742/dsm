from otter.test_files import test_case
import numpy as np
from datascience import *

OK_FORMAT = False

name = "q1_4"
points = 8

@test_case(points=4, hidden=True)
def test_mean(resampled_slopes):
    test_mean = np.mean(resampled_slopes)
    assert test_mean >= 0.70 and test_mean <= 0.73

@test_case(points=4, hidden=True)
def test_unique(resampled_slopes):
    assert len(np.unique(resampled_slopes)) == 1000
