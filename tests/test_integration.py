"""Integration tests for Geodude package."""

import sys
from pathlib import Path
from typing import List

import pytest

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from geodude import __author__, __version__, calculate_geohashes


class TestPackageIntegration:
    """Integration tests for the complete package."""

    def test_package_imports(self) -> None:
        """Test that all package imports work correctly."""
        # Test main package import
        import geodude

        # Test specific function import
        from geodude import calculate_geohashes

        # Test internal module import
        from geodude.cluster_functions import _calculate_single_geohash

        # All imports should work without errors
        assert hasattr(geodude, "calculate_geohashes")
        assert callable(calculate_geohashes)
        assert callable(_calculate_single_geohash)

    def test_package_metadata(self) -> None:
        """Test package metadata is accessible."""
        assert __version__ == "0.1.0"
        assert __author__ == "Odos Matthews"

        # Test that metadata is accessible through package
        import geodude

        assert hasattr(geodude, "__version__")
        assert hasattr(geodude, "__author__")

    def test_end_to_end_workflow(self) -> None:
        """Test complete end-to-end workflow."""
        # Simulate a real-world use case
        cities = [
            ("San Francisco", 37.7749, -122.4194),
            ("New York", 40.7128, -74.0060),
            ("London", 51.5074, -0.1278),
            ("Tokyo", 35.6762, 139.6503),
            ("Sydney", -33.8688, 151.2093),
        ]

        # Extract coordinates
        lats = [city[1] for city in cities]
        lons = [city[2] for city in cities]

        # Calculate geohashes
        hashes = calculate_geohashes(lats, lons, 5)

        # Verify results
        assert len(hashes) == len(cities)
        assert all(isinstance(h, str) for h in hashes)
        assert all(len(h) == 5 for h in hashes)

        # Verify each city has a unique geohash
        assert len(set(hashes)) == len(hashes)

    def test_caching_across_multiple_calls(self) -> None:
        """Test caching behavior across multiple function calls."""
        lats = [37.7749, 40.7128]
        lons = [-122.4194, -74.0060]

        # Multiple calls with same parameters
        results = []
        for _ in range(10):
            hashes = calculate_geohashes(lats, lons, 5)
            results.append(hashes)

        # All results should be identical
        first_result = results[0]
        for result in results[1:]:
            assert result == first_result

    def test_mixed_precision_workflow(self) -> None:
        """Test workflow with mixed precision levels."""
        lats = [37.7749, 40.7128, 51.5074]
        lons = [-122.4194, -74.0060, -0.1278]

        # Calculate with different precision levels
        precision_results = {}
        for precision in [1, 3, 5, 8]:
            hashes = calculate_geohashes(lats, lons, precision)
            precision_results[precision] = hashes

            # Verify results
            assert len(hashes) == len(lats)
            assert all(len(h) == precision for h in hashes)

        # Verify that higher precision gives more specific results
        # (results should be different for different precisions)
        assert precision_results[1] != precision_results[3]
        assert precision_results[3] != precision_results[5]
        assert precision_results[5] != precision_results[8]


class TestErrorHandlingIntegration:
    """Integration tests for error handling."""

    def test_comprehensive_error_handling(self) -> None:
        """Test comprehensive error handling scenarios."""
        # Test various error conditions
        error_cases = [
            # Invalid latitude
            ([91.0], [0.0], 5, "Latitude must be between -90 and 90"),
            ([-91.0], [0.0], 5, "Latitude must be between -90 and 90"),
            # Invalid longitude
            ([0.0], [181.0], 5, "Longitude must be between -180 and 180"),
            ([0.0], [-181.0], 5, "Longitude must be between -180 and 180"),
            # Invalid precision
            ([0.0], [0.0], 0, "Precision must be between 1 and 12"),
            ([0.0], [0.0], 13, "Precision must be between 1 and 12"),
            # Mismatched lengths
            ([0.0, 1.0], [0.0], 5, "must have same length"),
        ]

        for lats, lons, precision, expected_error in error_cases:
            with pytest.raises(ValueError, match=expected_error):
                calculate_geohashes(lats, lons, precision)

    def test_error_recovery(self) -> None:
        """Test that errors don't corrupt the cache."""
        lats = [37.7749, 40.7128]
        lons = [-122.4194, -74.0060]

        # First, calculate valid hashes
        valid_hashes = calculate_geohashes(lats, lons, 5)

        # Then, try invalid input (should raise error)
        with pytest.raises(ValueError):
            calculate_geohashes([91.0], [0.0], 5)

        # Finally, calculate valid hashes again (should still work)
        recovered_hashes = calculate_geohashes(lats, lons, 5)

        # Results should be identical (cache should still work)
        assert valid_hashes == recovered_hashes


class TestPerformanceIntegration:
    """Integration tests for performance characteristics."""

    def test_scalability(self) -> None:
        """Test performance scalability with dataset size."""
        import time

        dataset_sizes = [10, 100, 1000]
        times = []

        for size in dataset_sizes:
            lats = [37.7749 + i * 0.001 for i in range(size)]
            lons = [-122.4194 + i * 0.001 for i in range(size)]

            start_time = time.time()
            hashes = calculate_geohashes(lats, lons, 5)
            end_time = time.time()

            times.append(end_time - start_time)
            assert len(hashes) == size

        # Performance should scale reasonably
        # (not necessarily linear, but shouldn't be exponential)
        assert times[2] < times[1] * 20  # 1000 items shouldn't take 20x longer than 100

    def test_memory_efficiency(self) -> None:
        """Test memory efficiency with large datasets."""
        import sys

        # Test with large dataset
        lats = [37.7749 + i * 0.001 for i in range(10000)]
        lons = [-122.4194 + i * 0.001 for i in range(10000)]

        # Measure memory usage
        initial_memory = sys.getsizeof([])
        hashes = calculate_geohashes(lats, lons, 5)
        final_memory = sys.getsizeof(hashes)

        # Memory usage should be reasonable
        memory_per_item = (final_memory - initial_memory) / len(hashes)
        assert memory_per_item < 100  # Less than 100 bytes per item

        # Verify results are correct
        assert len(hashes) == 10000
        assert all(isinstance(h, str) for h in hashes)


class TestRealWorldScenarios:
    """Tests for real-world usage scenarios."""

    def test_gps_tracking_simulation(self) -> None:
        """Simulate GPS tracking data processing."""
        # Simulate GPS coordinates from a moving vehicle
        import random

        random.seed(42)

        # Starting point (San Francisco)
        start_lat, start_lon = 37.7749, -122.4194

        # Generate simulated GPS track
        track_lats = []
        track_lons = []

        current_lat, current_lon = start_lat, start_lon
        for _ in range(100):
            # Simulate movement (small random changes)
            current_lat += random.uniform(-0.001, 0.001)
            current_lon += random.uniform(-0.001, 0.001)

            # Keep within valid ranges
            current_lat = max(-90, min(90, current_lat))
            current_lon = max(-180, min(180, current_lon))

            track_lats.append(current_lat)
            track_lons.append(current_lon)

        # Calculate geohashes for the track
        hashes = calculate_geohashes(track_lats, track_lons, 6)

        # Verify results
        assert len(hashes) == 100
        assert all(isinstance(h, str) for h in hashes)
        assert all(len(h) == 6 for h in hashes)

        # Most hashes should be similar (nearby coordinates)
        # but not all identical (movement should create variation)
        unique_hashes = len(set(hashes))
        assert unique_hashes > 1  # Should have some variation
        assert unique_hashes < 100  # But not completely unique

    def test_city_database_simulation(self) -> None:
        """Simulate processing a city database."""
        # Simulate a database of world cities
        cities_data = [
            ("San Francisco", 37.7749, -122.4194),
            ("New York", 40.7128, -74.0060),
            ("London", 51.5074, -0.1278),
            ("Tokyo", 35.6762, 139.6503),
            ("Sydney", -33.8688, 151.2093),
            ("Paris", 48.8566, 2.3522),
            ("Berlin", 52.5200, 13.4050),
            ("Moscow", 55.7558, 37.6176),
            ("Beijing", 39.9042, 116.4074),
            ("Mumbai", 19.0760, 72.8777),
        ]

        # Process cities in batches
        batch_size = 3
        all_hashes = []

        for i in range(0, len(cities_data), batch_size):
            batch = cities_data[i : i + batch_size]
            lats = [city[1] for city in batch]
            lons = [city[2] for city in batch]

            hashes = calculate_geohashes(lats, lons, 5)
            all_hashes.extend(hashes)

        # Verify results
        assert len(all_hashes) == len(cities_data)
        assert all(isinstance(h, str) for h in all_hashes)
        assert all(len(h) == 5 for h in all_hashes)

        # All cities should have unique geohashes
        assert len(set(all_hashes)) == len(all_hashes)

    def test_api_response_simulation(self) -> None:
        """Simulate processing API response data."""
        # Simulate API response with coordinate data
        api_response = {
            "locations": [
                {"name": "Location 1", "lat": 37.7749, "lon": -122.4194},
                {"name": "Location 2", "lat": 40.7128, "lon": -74.0060},
                {"name": "Location 3", "lat": 51.5074, "lon": -0.1278},
            ]
        }

        # Extract coordinates
        lats: List[float] = [float(loc["lat"]) for loc in api_response["locations"]]  # type: ignore[arg-type]
        lons: List[float] = [float(loc["lon"]) for loc in api_response["locations"]]  # type: ignore[arg-type]

        # Calculate geohashes
        hashes = calculate_geohashes(lats, lons, 5)

        # Create enriched response
        enriched_response = []
        for i, loc in enumerate(api_response["locations"]):
            enriched_response.append({**loc, "geohash": hashes[i]})

        # Verify enriched response
        assert len(enriched_response) == 3
        assert all("geohash" in loc for loc in enriched_response)
        assert all(isinstance(loc["geohash"], str) for loc in enriched_response)
