from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q5_6"
points = 4


@test_case(points=4, hidden=True)
def test_q5_6_value(total_revenue, sales):
    """
    Compute the expected total revenue dynamically and compare with total_revenue.
    """
    computed_value = sum(sales.column("count sold") * sales.column("price per fruit ($)"))  # Formula for total revenue
    assert abs(total_revenue - computed_value) < 0.01, f"Expected total_revenue to be {computed_value}, but got {total_revenue}"
