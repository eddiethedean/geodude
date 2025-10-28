"""Test utilities and helper functions."""

from typing import List, Tuple

import pytest

from geodude import calculate_geohashes


def assert_valid_geohash(geohash: str, precision: int) -> None:
    """Assert that a geohash is valid for the given precision."""
    assert isinstance(geohash, str), f"Geohash should be string, got {type(geohash)}"
    assert len(geohash) == precision, (
        f"Geohash length should be {precision}, got {len(geohash)}"
    )
    assert geohash.isalnum(), f"Geohash should be alphanumeric, got {geohash}"
    # Note: PyGeodesy may include 'u' in geohashes, so we only check for 'i', 'l', 'o'
    assert not any(c in "ilo" for c in geohash.lower()), (
        f"Geohash should not contain ambiguous characters i, l, o, got {geohash}"
    )


def assert_coordinate_lists_match(
    lats: List[float], lons: List[float], hashes: List[str]
) -> None:
    """Assert that coordinate lists and hashes have matching lengths."""
    assert len(lats) == len(lons), (
        "Latitude and longitude lists should have same length"
    )
    assert len(hashes) == len(lats), (
        "Hashes list should have same length as coordinate lists"
    )


def generate_test_coordinates(
    count: int, seed: int = 42
) -> Tuple[List[float], List[float]]:
    """Generate test coordinates for testing."""
    import random

    random.seed(seed)

    lats = [random.uniform(-90, 90) for _ in range(count)]
    lons = [random.uniform(-180, 180) for _ in range(count)]

    return lats, lons


def benchmark_geohash_calculation(
    lats: List[float], lons: List[float], precision: int, iterations: int = 1
) -> float:
    """Benchmark geohash calculation performance."""
    import time

    total_time: float = 0
    for _ in range(iterations):
        start_time = time.time()
        calculate_geohashes(lats, lons, precision)
        total_time += time.time() - start_time

    return total_time / iterations


class TestUtilities:
    """Test the utility functions."""

    def test_assert_valid_geohash(self) -> None:
        """Test the geohash validation utility."""
        # Valid geohashes
        assert_valid_geohash("9q8yy", 5)
        assert_valid_geohash("dr5rs", 5)
        assert_valid_geohash("gcpvj", 5)

        # Test with different precisions
        assert_valid_geohash("9", 1)
        assert_valid_geohash("9q8yyk7mgpu0", 12)

    def test_assert_coordinate_lists_match(self) -> None:
        """Test the coordinate list matching utility."""
        lats = [37.7749, 40.7128]
        lons = [-122.4194, -74.0060]
        hashes = ["9q8yy", "dr5rs"]

        # Should not raise
        assert_coordinate_lists_match(lats, lons, hashes)

        # Should raise for mismatched lengths
        with pytest.raises(AssertionError):
            assert_coordinate_lists_match([37.7749], lons, hashes)

    def test_generate_test_coordinates(self) -> None:
        """Test the coordinate generation utility."""
        lats, lons = generate_test_coordinates(10)

        assert len(lats) == 10
        assert len(lons) == 10

        # All coordinates should be within valid ranges
        assert all(-90 <= lat <= 90 for lat in lats)
        assert all(-180 <= lon <= 180 for lon in lons)

        # Same seed should produce same coordinates
        lats2, lons2 = generate_test_coordinates(10, seed=42)
        assert lats == lats2
        assert lons == lons2

    def test_benchmark_geohash_calculation(self) -> None:
        """Test the benchmarking utility."""
        lats, lons = generate_test_coordinates(100)

        # Benchmark should return a positive time
        avg_time = benchmark_geohash_calculation(lats, lons, 5, iterations=3)
        assert avg_time > 0

        # Multiple iterations should give consistent results
        times = []
        for _ in range(5):
            time_taken = benchmark_geohash_calculation(lats, lons, 5, iterations=1)
            times.append(time_taken)

        # All times should be positive and reasonably consistent
        assert all(t > 0 for t in times)
        assert max(times) / min(times) < 10  # Should not vary by more than 10x


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_floating_point_precision(self) -> None:
        """Test handling of floating point precision issues."""
        # Use coordinates with many decimal places
        lats = [37.774900000000001, 40.712800000000002]
        lons = [-122.41940000000001, -74.006000000000002]

        hashes = calculate_geohashes(lats, lons, 5)

        assert len(hashes) == 2
        assert all(isinstance(h, str) for h in hashes)

    def test_very_small_coordinates(self) -> None:
        """Test with very small coordinate values."""
        lats = [0.000001, -0.000001]
        lons = [0.000001, -0.000001]

        hashes = calculate_geohashes(lats, lons, 5)

        assert len(hashes) == 2
        assert all(isinstance(h, str) for h in hashes)

    def test_coordinates_near_boundaries(self) -> None:
        """Test coordinates very close to boundaries."""
        boundary_cases = [
            ([89.999999], [179.999999]),
            ([-89.999999], [-179.999999]),
            ([0.000001], [0.000001]),
            ([-0.000001], [-0.000001]),
        ]

        for lats, lons in boundary_cases:
            hashes = calculate_geohashes(lats, lons, 5)
            assert len(hashes) == 1
            assert isinstance(hashes[0], str)

    def test_repeated_coordinates(self) -> None:
        """Test with repeated coordinate values."""
        lats = [37.7749, 37.7749, 37.7749]
        lons = [-122.4194, -122.4194, -122.4194]

        hashes = calculate_geohashes(lats, lons, 5)

        # All hashes should be identical
        assert len(hashes) == 3
        assert all(h == hashes[0] for h in hashes)

    def test_alternating_coordinates(self) -> None:
        """Test with alternating coordinate patterns."""
        lats = [37.7749, -37.7749, 37.7749, -37.7749]
        lons = [-122.4194, 122.4194, -122.4194, 122.4194]

        hashes = calculate_geohashes(lats, lons, 5)

        assert len(hashes) == 4
        assert all(isinstance(h, str) for h in hashes)

        # First and third should be identical
        assert hashes[0] == hashes[2]
        # Second and fourth should be identical
        assert hashes[1] == hashes[3]
        # First and second should be different
        assert hashes[0] != hashes[1]
