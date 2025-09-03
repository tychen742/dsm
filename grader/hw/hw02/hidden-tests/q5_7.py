from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q5_7"
points = 5

@test_case(points=2, hidden=False)
def test_q5_7_table_structure(remaining_inventory):
    """
    Check if remaining_inventory is a Table and has the correct columns.
    """
    from datascience import Table
    expected_columns = ["box ID", "fruit name", "count"]
    
    assert isinstance(remaining_inventory, Table), \
        f"Expected `remaining_inventory` to be a Table, but got {type(remaining_inventory)}"
    
    assert remaining_inventory.labels == tuple(expected_columns), \
        f"Expected columns {expected_columns}, but got {remaining_inventory.labels}"

@test_case(points=3, hidden=False)
def test_q5_7_kiwi_peach_count(remaining_inventory, inventory, sales):
    """
    Check if the remaining count for kiwi and peach are correctly computed.
    Instead of hardcoding, dynamically compute the expected values.
    """
    # Compute expected counts dynamically
    kiwi_original = inventory.where("fruit name", "kiwi").column("count").item(0)
    kiwi_sold = sales.where("fruit name", "kiwi").column("count sold").item(0)
    expected_kiwi = kiwi_original - kiwi_sold

    peach_original = inventory.where("fruit name", "peach").column("count").item(0)
    peach_sold = sales.where("fruit name", "peach").column("count sold").item(0)
    expected_peach = peach_original - peach_sold

    # Get actual values
    actual_kiwi = remaining_inventory.where("fruit name", "kiwi").column("count").item(0)
    actual_peach = remaining_inventory.where("fruit name", "peach").column("count").item(0)

    # Assertions
    assert actual_kiwi == expected_kiwi, \
        f"Expected kiwi count {expected_kiwi}, but got {actual_kiwi}"

    assert actual_peach == expected_peach, \
        f"Expected peach count {expected_peach}, but got {actual_peach}"