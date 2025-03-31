import pytest
from dstruct.grader import load_data,overallocation, conflicts, under_support, unwilling, un_preferred
import numpy as np

@pytest.fixture
def a():
    a = np.loadtxt('test1.csv', delimiter=',')
    return a
@pytest.fixture
def b():
    b = np.loadtxt('test2.csv', delimiter=',')
    return b
@pytest.fixture
def c():
    c = np.loadtxt('test3.csv', delimiter=',')
    return c
@pytest.fixture
def willing():
    willing, required, avail, timeslots = load_data()
    return willing
@pytest.fixture
def required():
    willing, required, avail, timeslots = load_data()
    return required
@pytest.fixture
def avail():
    willing, required, avail, timeslots = load_data()
    return avail
@pytest.fixture
def timeslots():
    willing, required, avail, timeslots = load_data()
    return timeslots

def test_grade_a(a):
    assert overallocation(a) == 37, f"Expected 37, got {overallocation(a)}"
    assert conflicts(a) == 8, f"Expected 8, got {conflicts(a)}"
    assert under_support(a) == 1, f"Expected 1, got {under_support(a)}"
    assert unwilling(a) == 53, f"Expected 53, got {unwilling(a)}"
    assert un_preferred(a) == 15, f"Expected 15, got {un_preferred(a)}"

def test_grade_b(b):
    assert overallocation(b) == 41, f"Expected 41, got {overallocation(b)}"
    assert conflicts(b) == 5, f"Expected 5, got {conflicts(b)}"
    assert under_support(b) == 0, f"Expected 0, got {under_support(b)}"
    assert unwilling(b) == 58, f"Expected 58, got {unwilling(b)}"
    assert un_preferred(b) == 19, f"Expected 19, got {un_preferred(b)}"

def test_grade_c(c):
    assert overallocation(c) == 23, f"Expected 23, got {overallocation(c)}"
    assert conflicts(c) == 2, f"Expected 2, got {conflicts(c)}"
    assert under_support(c) == 7, f"Expected 7, got {under_support(c)}"
    assert unwilling(c) == 43, f"Expected 43, got {unwilling(c)}"
    assert un_preferred(c) == 10, f"Expected 10, got {un_preferred(c)}"
def time_profile():
    pass