"""Test configuration and fixtures for Geodude package."""

from typing import List, Tuple

import pytest


@pytest.fixture
def sample_coordinates() -> Tuple[List[float], List[float]]:
    """Sample coordinates for testing."""
    lats = [37.7749, 40.7128, 51.5074, -33.8688, 35.6762]
    lons = [-122.4194, -74.0060, -0.1278, 151.2093, 139.6503]
    return lats, lons


@pytest.fixture
def sample_coordinates_single() -> Tuple[float, float]:
    """Single coordinate pair for testing."""
    return 37.7749, -122.4194


@pytest.fixture
def invalid_coordinates() -> Tuple[List[float], List[float]]:
    """Invalid coordinates for testing error cases."""
    lats = [91.0, -91.0, 0.0]  # Invalid latitudes
    lons = [181.0, -181.0, 0.0]  # Invalid longitudes
    return lats, lons


@pytest.fixture
def mismatched_coordinates() -> Tuple[List[float], List[float]]:
    """Mismatched length coordinates for testing error cases."""
    lats = [37.7749, 40.7128]
    lons = [-122.4194]  # Different length
    return lats, lons


@pytest.fixture
def empty_coordinates() -> Tuple[List[float], List[float]]:
    """Empty coordinate lists for testing."""
    return [], []


@pytest.fixture
def precision_levels() -> List[int]:
    """Valid precision levels for testing."""
    return [1, 5, 8, 12]


@pytest.fixture
def invalid_precision_levels() -> List[int]:
    """Invalid precision levels for testing error cases."""
    return [0, -1, 13, 20]
