from otter.test_files import test_case
import numpy as np
from datascience import *

OK_FORMAT = False

name = "q2_4"
points = 6

@test_case(points=3, hidden=True)
def test_mean(predictions_for_eight):
    test_mean = np.round(np.mean(predictions_for_eight), 2)
    assert np.isclose(test_mean, 5.69)

@test_case(points=3, hidden=True)
def test_unique(predictions_for_eight):
    assert len(np.unique(predictions_for_eight)) == 1000
