"""GeoHash calculation functions using PyGeodesy."""

from functools import lru_cache
from typing import List

from pygeodesy import geohash


@lru_cache(maxsize=10000)
def _calculate_single_geohash(lat: float, lon: float, precision: int) -> str:
    """Calculate a single geohash with caching.

    Args:
        lat: Latitude in decimal degrees
        lon: Longitude in decimal degrees
        precision: Geohash precision (1-12)

    Returns:
        Geohash string

    Raises:
        ValueError: If coordinates are out of valid range
    """
    if not (-90 <= lat <= 90):
        raise ValueError(f"Latitude must be between -90 and 90, got {lat}")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Longitude must be between -180 and 180, got {lon}")
    if not (1 <= precision <= 12):
        raise ValueError(f"Precision must be between 1 and 12, got {precision}")

    return geohash.encode(lat, lon, precision)  # type: ignore[no-any-return]


def calculate_geohashes(
    lats: List[float], lons: List[float], precision: int
) -> List[str]:
    """Calculate geohashes for a list of coordinates.

    Args:
        lats: List of latitudes in decimal degrees
        lons: List of longitudes in decimal degrees
        precision: Geohash precision (1-12)

    Returns:
        List of geohash strings

    Raises:
        ValueError: If input lists have different lengths or invalid coordinates

    Example:
        >>> lats = [37.7749, 40.7128]
        >>> lons = [-122.4194, -74.0060]
        >>> hashes = calculate_geohashes(lats, lons, 5)
        >>> print(hashes)
        ['9q8yy', 'dr5rs']
    """
    if len(lats) != len(lons):
        raise ValueError(
            f"Latitude and longitude lists must have same length, got {len(lats)} and {len(lons)}"
        )

    if not lats:
        return []

    return [
        _calculate_single_geohash(lat, lon, precision) for lat, lon in zip(lats, lons)
    ]
