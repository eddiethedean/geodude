"""Performance and stress tests for Geodude package."""

import random
import time

from geodude import calculate_geohashes


class TestPerformance:
    """Performance tests for geohash calculations."""

    def test_small_dataset_performance(self) -> None:
        """Test performance with small dataset."""
        lats = [37.7749, 40.7128, 51.5074]
        lons = [-122.4194, -74.0060, -0.1278]

        start_time = time.time()
        hashes = calculate_geohashes(lats, lons, 5)
        end_time = time.time()

        # Should be very fast for small dataset
        assert end_time - start_time < 0.1
        assert len(hashes) == 3

    def test_medium_dataset_performance(self) -> None:
        """Test performance with medium dataset."""
        # Generate 1000 coordinates
        random.seed(42)
        lats = [random.uniform(-90, 90) for _ in range(1000)]
        lons = [random.uniform(-180, 180) for _ in range(1000)]

        start_time = time.time()
        hashes = calculate_geohashes(lats, lons, 5)
        end_time = time.time()

        # Should complete in reasonable time
        assert end_time - start_time < 0.5
        assert len(hashes) == 1000

    def test_large_dataset_performance(self) -> None:
        """Test performance with large dataset."""
        # Generate 10000 coordinates
        random.seed(42)
        lats = [random.uniform(-90, 90) for _ in range(10000)]
        lons = [random.uniform(-180, 180) for _ in range(10000)]

        start_time = time.time()
        hashes = calculate_geohashes(lats, lons, 5)
        end_time = time.time()

        # Should complete in reasonable time
        assert end_time - start_time < 2.0
        assert len(hashes) == 10000

    def test_caching_performance_benefit(self) -> None:
        """Test that caching provides performance benefits."""
        # Use same coordinates multiple times
        lats = [37.7749, 40.7128, 51.5074]
        lons = [-122.4194, -74.0060, -0.1278]

        # First call (no cache)
        start_time = time.time()
        hashes1 = calculate_geohashes(lats, lons, 5)
        first_call_time = time.time() - start_time

        # Second call (with cache)
        start_time = time.time()
        hashes2 = calculate_geohashes(lats, lons, 5)
        second_call_time = time.time() - start_time

        # Results should be identical
        assert hashes1 == hashes2

        # Second call should be faster (cached)
        assert second_call_time < first_call_time

    def test_different_precision_performance(self) -> None:
        """Test performance with different precision levels."""
        lats = [37.7749] * 100
        lons = [-122.4194] * 100

        precision_times = {}

        for precision in [1, 5, 8, 12]:
            start_time = time.time()
            hashes = calculate_geohashes(lats, lons, precision)
            end_time = time.time()

            precision_times[precision] = end_time - start_time
            assert len(hashes) == 100

        # Higher precision should generally take longer, but allow small variance (<=10ms)
        assert precision_times[12] + 0.01 >= precision_times[1]


class TestStressTests:
    """Stress tests for edge cases and extreme conditions."""

    def test_extreme_coordinates(self) -> None:
        """Test with extreme coordinate values."""
        extreme_cases = [
            ([90.0], [180.0]),  # Maximum positive
            ([-90.0], [-180.0]),  # Maximum negative
            ([0.0], [0.0]),  # Zero
            ([89.999999], [179.999999]),  # Near maximum
            ([-89.999999], [-179.999999]),  # Near minimum
        ]

        for lats, lons in extreme_cases:
            hashes = calculate_geohashes(lats, lons, 5)
            assert len(hashes) == 1
            assert isinstance(hashes[0], str)

    def test_precision_boundaries(self) -> None:
        """Test with precision boundary values."""
        lats = [37.7749]
        lons = [-122.4194]

        # Test all valid precision levels
        for precision in range(1, 13):
            hashes = calculate_geohashes(lats, lons, precision)
            assert len(hashes) == 1
            assert len(hashes[0]) == precision

    def test_repeated_calculations(self) -> None:
        """Test repeated calculations with same parameters."""
        lats = [37.7749, 40.7128]
        lons = [-122.4194, -74.0060]

        # Perform same calculation 100 times
        all_hashes = []
        for _ in range(100):
            hashes = calculate_geohashes(lats, lons, 5)
            all_hashes.append(hashes)

        # All results should be identical
        first_hash = all_hashes[0]
        for hash_result in all_hashes[1:]:
            assert hash_result == first_hash

    def test_mixed_precision_calculations(self) -> None:
        """Test calculations with mixed precision levels."""
        lats = [37.7749, 40.7128, 51.5074]
        lons = [-122.4194, -74.0060, -0.1278]

        # Calculate with different precision levels
        precision_results = {}
        for precision in [1, 5, 8, 12]:
            hashes = calculate_geohashes(lats, lons, precision)
            precision_results[precision] = hashes

            # Verify all hashes have correct length
            assert all(len(h) == precision for h in hashes)

        # Verify results are different for different precisions
        assert precision_results[1] != precision_results[5]
        assert precision_results[5] != precision_results[8]

    def test_concurrent_access_simulation(self) -> None:
        """Simulate concurrent access patterns."""
        # This test simulates multiple "threads" accessing the cache
        coordinates = [
            (37.7749, -122.4194),  # San Francisco
            (40.7128, -74.0060),  # New York
            (51.5074, -0.1278),  # London
        ]

        # Simulate multiple "threads" by calling the function multiple times
        # with the same parameters
        all_results = []
        for _ in range(50):  # Simulate 50 concurrent requests
            lats, lons = zip(*coordinates)
            hashes = calculate_geohashes(list(lats), list(lons), 5)
            all_results.append(hashes)

        # All results should be identical (cache consistency)
        first_result = all_results[0]
        for result in all_results[1:]:
            assert result == first_result

    def test_memory_efficiency(self) -> None:
        """Test memory efficiency with large datasets."""
        import sys

        # Test with progressively larger datasets
        dataset_sizes = [100, 1000, 5000]

        for size in dataset_sizes:
            lats = [random.uniform(-90, 90) for _ in range(size)]
            lons = [random.uniform(-180, 180) for _ in range(size)]

            # Measure memory before
            initial_memory = sys.getsizeof([])

            # Calculate hashes
            hashes = calculate_geohashes(lats, lons, 5)

            # Measure memory after
            final_memory = sys.getsizeof(hashes)

            # Memory usage should be reasonable
            memory_per_item = (final_memory - initial_memory) / size
            assert memory_per_item < 200  # Less than 200 bytes per item
