"""Tests for cluster_functions module."""

from typing import List, Tuple

import pytest

from geodude.cluster_functions import _calculate_single_geohash, calculate_geohashes


class TestCalculateSingleGeohash:
    """Test the internal _calculate_single_geohash function."""

    def test_basic_functionality(
        self, sample_coordinates_single: Tuple[float, float]
    ) -> None:
        """Test basic single geohash calculation."""
        lat, lon = sample_coordinates_single
        hash_value = _calculate_single_geohash(lat, lon, 5)

        assert isinstance(hash_value, str)
        assert len(hash_value) == 5

    def test_caching(self, sample_coordinates_single: Tuple[float, float]) -> None:
        """Test that caching works for single geohash calculation."""
        lat, lon = sample_coordinates_single

        # First call
        hash1 = _calculate_single_geohash(lat, lon, 5)

        # Second call should return same result (cached)
        hash2 = _calculate_single_geohash(lat, lon, 5)

        assert hash1 == hash2

    def test_different_precisions(
        self, sample_coordinates_single: Tuple[float, float]
    ) -> None:
        """Test single geohash with different precision levels."""
        lat, lon = sample_coordinates_single

        for precision in range(1, 13):
            hash_value = _calculate_single_geohash(lat, lon, precision)
            assert len(hash_value) == precision
            assert isinstance(hash_value, str)

    def test_invalid_latitude(self) -> None:
        """Test error handling for invalid latitude in single geohash."""
        with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
            _calculate_single_geohash(91.0, 0.0, 5)

        with pytest.raises(ValueError, match="Latitude must be between -90 and 90"):
            _calculate_single_geohash(-91.0, 0.0, 5)

    def test_invalid_longitude(self) -> None:
        """Test error handling for invalid longitude in single geohash."""
        with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
            _calculate_single_geohash(0.0, 181.0, 5)

        with pytest.raises(ValueError, match="Longitude must be between -180 and 180"):
            _calculate_single_geohash(0.0, -181.0, 5)

    def test_invalid_precision(
        self, sample_coordinates_single: Tuple[float, float]
    ) -> None:
        """Test error handling for invalid precision in single geohash."""
        lat, lon = sample_coordinates_single

        with pytest.raises(ValueError, match="Precision must be between 1 and 12"):
            _calculate_single_geohash(lat, lon, 0)

        with pytest.raises(ValueError, match="Precision must be between 1 and 12"):
            _calculate_single_geohash(lat, lon, 13)

    def test_boundary_values(self) -> None:
        """Test single geohash with boundary coordinate values."""
        boundary_cases = [
            (90.0, 180.0, 5),
            (-90.0, -180.0, 5),
            (0.0, 0.0, 5),
        ]

        for lat, lon, precision in boundary_cases:
            hash_value = _calculate_single_geohash(lat, lon, precision)
            assert isinstance(hash_value, str)
            assert len(hash_value) == precision

    def test_known_coordinates(self) -> None:
        """Test single geohash with known coordinates."""
        # San Francisco coordinates
        lat, lon = 37.7749, -122.4194

        # Test with different precision levels
        test_cases = [
            (1, "9"),
            (2, "9q"),
            (3, "9q8"),
            (4, "9q8y"),
            (5, "9q8yy"),
        ]

        for precision, expected_prefix in test_cases:
            hash_value = _calculate_single_geohash(lat, lon, precision)
            assert hash_value.startswith(expected_prefix)
            assert len(hash_value) == precision


class TestCalculateGeohashesIntegration:
    """Integration tests for calculate_geohashes function."""

    def test_consistency_with_single_function(
        self, sample_coordinates: Tuple[List[float], List[float]]
    ) -> None:
        """Test that calculate_geohashes is consistent with _calculate_single_geohash."""
        lats, lons = sample_coordinates
        precision = 5

        # Calculate using batch function
        batch_hashes = calculate_geohashes(lats, lons, precision)

        # Calculate using single function
        single_hashes = [
            _calculate_single_geohash(lat, lon, precision)
            for lat, lon in zip(lats, lons)
        ]

        assert batch_hashes == single_hashes

    def test_caching_across_functions(
        self, sample_coordinates_single: Tuple[float, float]
    ) -> None:
        """Test that caching works across both functions."""
        lat, lon = sample_coordinates_single
        precision = 5

        # Call single function first
        single_hash = _calculate_single_geohash(lat, lon, precision)

        # Call batch function - should use cached result
        batch_hashes = calculate_geohashes([lat], [lon], precision)

        assert batch_hashes[0] == single_hash

    def test_performance_with_large_dataset(self) -> None:
        """Test performance with large dataset."""
        import time

        # Generate large dataset
        lats = [37.7749 + i * 0.001 for i in range(1000)]
        lons = [-122.4194 + i * 0.001 for i in range(1000)]

        start_time = time.time()
        hashes = calculate_geohashes(lats, lons, 5)
        end_time = time.time()

        # Should complete in reasonable time (less than 1 second)
        assert end_time - start_time < 1.0
        assert len(hashes) == 1000

    def test_memory_usage(self) -> None:
        """Test that memory usage is reasonable."""
        import sys

        # Calculate hashes for many coordinates
        lats = [37.7749 + i * 0.001 for i in range(10000)]
        lons = [-122.4194 + i * 0.001 for i in range(10000)]

        initial_memory = sys.getsizeof([])
        hashes = calculate_geohashes(lats, lons, 5)
        final_memory = sys.getsizeof(hashes)

        # Memory usage should be reasonable
        memory_per_hash = (final_memory - initial_memory) / len(hashes)
        assert memory_per_hash < 100  # Less than 100 bytes per hash
