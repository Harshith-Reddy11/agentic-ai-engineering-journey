
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1])
)

import pytest
from agent import validate_goal


def test_valid_goal():
    assert validate_goal("  Calculate 5 + 5  ") == "Calculate 5 + 5"


def test_empty_goal():
    with pytest.raises(ValueError, match="Goal cannot be empty"):
        validate_goal("")


def test_whitespace_goal():
    with pytest.raises(ValueError, match="Goal cannot be empty"):
        validate_goal("   ")


def test_non_string_goal():
    with pytest.raises(TypeError, match="Goal must be a string"):
        validate_goal(123)


def test_excessively_long_goal():
    with pytest.raises(ValueError, match="Goal is too long"):
        validate_goal("a" * 2001)
