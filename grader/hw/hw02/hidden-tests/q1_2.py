from otter.test_files import test_case
import numpy as np
from datascience import *
import math

OK_FORMAT = False

name = "q1_2"
points = 4  


@test_case(points=1, hidden=True)
def test_q1_2_type(book_title_words):
    assert isinstance(book_title_words, np.ndarray), "book_title_words should be a NumPy array."

@test_case(points=1, hidden=True)
def test_q1_2_length(book_title_words):
    assert len(book_title_words) == 3, f"Expected array length of 3, but got {len(book_title_words)}."

@test_case(points=2, hidden=True)
def test_q1_2_values(book_title_words):
    expected_values = np.array(["Eats", "Shoots", "and Leaves"])
    assert np.array_equal(book_title_words, expected_values), \
        f"Expected values {expected_values}, but got {book_title_words}."

# @test_case(points=1, hidden=True)
# def test_q1_2_format(book_title_words):
#     assert not any(',' in text for text in book_title_words), \
#         "Elements in book_title_words should not contain commas."