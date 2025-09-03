from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q4_1"
points = 6

@test_case(points=1.5, hidden=True)
def test_q4_1_shortest(waiting_times, shortest):
    """
    Verify that the shortest waiting time is correctly assigned.
    """
    expected_shortest = np.min(waiting_times)
    assert shortest == expected_shortest, f"Expected shortest {expected_shortest}, but got {shortest}"

@test_case(points=1.5, hidden=True)
def test_q4_1_longest(waiting_times, longest):
    """
    Verify that the longest waiting time is correctly assigned.
    """
    expected_longest = np.max(waiting_times)
    assert longest == expected_longest, f"Expected longest {expected_longest}, but got {longest}"

@test_case(points=1.5, hidden=True)
def test_q4_1_average(waiting_times, average):
    """
    Verify that the average waiting time is correctly computed.
    """
    expected_average = np.mean(waiting_times)
    assert np.isclose(average, expected_average, atol=0.1), f"Expected average {expected_average}, but got {average}"

@test_case(points=1.5, hidden=True)
def test_q4_1_order(shortest, longest, average):
    """
    Verify the logical order: shortest <= average <= longest.
    """
    assert shortest <= average <= longest, \
        f"Expected order shortest ({shortest}) <= average ({average}) <= longest ({longest})"