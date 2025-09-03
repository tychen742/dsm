from otter.test_files import test_case
import numpy as np
from datascience import *

OK_FORMAT = False

name = "q2_2"
points = 4

@test_case(points=4, hidden=True)
def test_value(experts_egg):
    assert np.isclose(experts_egg, 6.408365842108825)
