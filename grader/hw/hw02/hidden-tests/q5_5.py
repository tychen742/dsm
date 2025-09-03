from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q5_5"
points = 4

@test_case(points=4, hidden=True)
def test_q5_5_value(total_fruits_sold):
    """
    Test that `total_fruits_sold` is correctly calculated as the sum of all fruits sold.
    """
    import numpy as np

# Convert to integer if total_fruits_sold is a NumPy array ## issue with garrison haleys code as shown below
#     total_fruits_sold = count_sold = sales.column("count sold")
# total_fruits_sold = np.sum(count_sold)
# total_fruits_sold
    total_fruits_sold_value = int(np.sum(total_fruits_sold)) if isinstance(total_fruits_sold, np.ndarray) else total_fruits_sold

    expected_value = 638  
    assert total_fruits_sold_value == expected_value, \
        f"Expected `total_fruits_sold` to be {expected_value}, but got {total_fruits_sold_value}."

