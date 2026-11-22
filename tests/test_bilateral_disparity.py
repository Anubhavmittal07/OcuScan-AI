import pytest

def check_bilateral_disparity(hb_left: float, hb_right: float, max_allowed: float = 1.8) -> bool:
    """Returns True if discrepancy is within acceptable clinical bounds."""
    diff = abs(hb_left - hb_right)
    return diff <= max_allowed

def test_bilateral_concordance_within_bounds():
    assert check_bilateral_disparity(12.4, 12.8) is True
    assert check_bilateral_disparity(10.1, 11.2) is True

def test_bilateral_disparity_exceeded():
    assert check_bilateral_disparity(10.0, 12.5) is False
    assert check_bilateral_disparity(8.0, 10.5) is False
