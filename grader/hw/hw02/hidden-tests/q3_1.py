from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q3_1"
points = 4 

@test_case(points=4, hidden=True)
def test_q3_1_values(first_product, second_product, third_product, fourth_product):
    expected_values = [42 * 157, -4224 * 157, 424224242 * 157, 250 * 157]
    
    assert first_product == expected_values[0], f"Expected {expected_values[0]}, but got {first_product}."
    assert second_product == expected_values[1], f"Expected {expected_values[1]}, but got {second_product}."
    assert third_product == expected_values[2], f"Expected {expected_values[2]}, but got {third_product}."
    assert fourth_product == expected_values[3], f"Expected {expected_values[3]}, but got {fourth_product}."

