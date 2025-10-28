"""Tests for the main geodude package functionality."""

from typing import List, Tuple

import pytest

from geodude import __author__, __version__, calculate_geohashes


class TestPackageMetadata:
    """Test package metadata."""

    def test_version(self) -> None:
        """Test that version is defined."""
        assert __version__ == "0.1.0"

    def test_author(self) -> None:
        """Test that author is defined."""
        assert __author__ == "Odos Matthews"


class TestCalculateGeohashes:
    """Test the main calculate_geohashes function."""

    def test_basic_functionality(
        self, sample_coordinates: Tuple[List[float], List[float]]
    ) -> None:
        """Test basic geohash calculation."""
        lats, lons = sample_coordinates
        hashes = calculate_geohashes(lats, lons, 5)

        assert len(hashes) == len(lats)
        assert all(isinstance(h, str) for h in hashes)
        assert all(len(h) == 5 for h in hashes)

    def test_different_precisions(
        self,
        sample_coordinates_single: Tuple[float, float],
        precision_levels: List[int],
    ) -> None:
        """Test geohash calculation with different precision levels."""
        lat, lon = sample_coordinates_single

        for precision in precision_levels:
            hashes = calculate_geohashes([lat], [lon], precision)
            assert len(hashes) == 1
            assert len(hashes[0]) == precision

    def test_empty_input(
        self, empty_coordinates: Tuple[List[float], List[float]]
    ) -> None:
        """Test geohash calculation with empty input."""
        lats, lons = empty_coordinates
        hashes = calculate_geohashes(lats, lons, 5)
        assert hashes == []

    def test_single_coordinate(
        self, sample_coordinates_single: Tuple[float, float]
    ) -> None:
        """Test geohash calculation with single coordinate."""
        lat, lon = sample_coordinates_single
        hashes = calculate_geohashes([lat], [lon], 5)

        assert len(hashes) == 1
        assert isinstance(hashes[0], str)
        assert len(hashes[0]) == 5

    def test_caching_behavior(
        self, sample_coordinates_single: Tuple[float, float]
    ) -> None:
        """Test that caching works correctly."""
        lat, lon = sample_coordinates_single

        # First call
        hashes1 = calculate_geohashes([lat], [lon], 5)

        # Second call with same parameters should return same result
        hashes2 = calculate_geohashes([lat], [lon], 5)

        assert hashes1 == hashes2

    def test_known_coordinates(self) -> None:
        """Test with known coordinates and expected geohashes."""
        # San Francisco coordinates
        lats = [37.7749]
        lons = [-122.4194]

        # Test different precision levels with known results
        test_cases = [
            (1, "9"),
            (2, "9q"),
            (3, "9q8"),
            (4, "9q8y"),
            (5, "9q8yy"),
        ]

        for precision, expected_prefix in test_cases:
            hashes = calculate_geohashes(lats, lons, precision)
            assert hashes[0].startswith(expected_prefix)

    def test_mismatched_lengths(
        self, mismatched_coordinates: Tuple[List[float], List[float]]
    ) -> None:
        """Test error handling for mismatched coordinate lengths."""
        lats, lons = mismatched_coordinates

        with pytest.raises(ValueError, match="must have same length"):
            calculate_geohashes(lats, lons, 5)

    def test_invalid_latitude(self) -> None:
        """Test error handling for invalid latitude."""
        lats = [91.0]  # Invalid latitude
        lons = [0.0]

        with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
            calculate_geohashes(lats, lons, 5)

    def test_invalid_longitude(self) -> None:
        """Test error handling for invalid longitude."""
        lats = [0.0]
        lons = [181.0]  # Invalid longitude

        with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
            calculate_geohashes(lats, lons, 5)

    def test_invalid_precision(
        self, sample_coordinates_single: Tuple[float, float]
    ) -> None:
        """Test error handling for invalid precision."""
        lat, lon = sample_coordinates_single

        # Test precision too low
        with pytest.raises(ValueError, match="Precision must be between 1 and 12"):
            calculate_geohashes([lat], [lon], 0)

        # Test precision too high
        with pytest.raises(ValueError, match="Precision must be between 1 and 12"):
            calculate_geohashes([lat], [lon], 13)

    def test_boundary_values(self) -> None:
        """Test geohash calculation with boundary coordinate values."""
        # Test exact boundary values
        boundary_cases = [
            (90.0, 180.0),  # Maximum values
            (-90.0, -180.0),  # Minimum values
            (0.0, 0.0),  # Zero values
        ]

        for lat, lon in boundary_cases:
            hashes = calculate_geohashes([lat], [lon], 5)
            assert len(hashes) == 1
            assert isinstance(hashes[0], str)

    def test_negative_coordinates(self) -> None:
        """Test geohash calculation with negative coordinates."""
        lats = [-33.8688, -22.9068]  # Sydney, Rio de Janeiro
        lons = [151.2093, -43.1729]

        hashes = calculate_geohashes(lats, lons, 5)

        assert len(hashes) == 2
        assert all(isinstance(h, str) for h in hashes)
        assert all(len(h) == 5 for h in hashes)

    def test_large_coordinate_lists(self) -> None:
        """Test geohash calculation with large coordinate lists."""
        # Generate 1000 random coordinates
        import random

        random.seed(42)  # For reproducible tests

        lats = [random.uniform(-90, 90) for _ in range(1000)]
        lons = [random.uniform(-180, 180) for _ in range(1000)]

        hashes = calculate_geohashes(lats, lons, 5)

        assert len(hashes) == 1000
        assert all(isinstance(h, str) for h in hashes)
        assert all(len(h) == 5 for h in hashes)

    def test_consistency_across_calls(
        self, sample_coordinates: Tuple[List[float], List[float]]
    ) -> None:
        """Test that results are consistent across multiple calls."""
        lats, lons = sample_coordinates

        # Multiple calls should return identical results
        hashes1 = calculate_geohashes(lats, lons, 5)
        hashes2 = calculate_geohashes(lats, lons, 5)
        hashes3 = calculate_geohashes(lats, lons, 5)

        assert hashes1 == hashes2 == hashes3
