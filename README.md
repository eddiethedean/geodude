# Geodude

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

Geodude calculates [GeoHashes](https://en.wikipedia.org/wiki/Geohash) for batches of latitude and longitude coordinates in Python. It supports precisions from 1 to 12 characters and validates coordinates and input lengths.

## Install

```bash
python -m pip install geodude
```

Geodude supports Python 3.8 and newer.

## Quick start

Pass latitude and longitude values in matching lists. Coordinates use decimal degrees, with latitude first and longitude second.

```python
from geodude import calculate_geohashes

lats = [37.7749, 40.7128, 51.5074]  # San Francisco, New York, London
lons = [-122.4194, -74.0060, -0.1278]

hashes = calculate_geohashes(lats, lons, precision=5)
print(hashes)
# ['9q8yy', 'dr5re', 'gcpvj']
```

Precision controls the number of characters in each hash. A longer hash identifies a smaller geographic area:

```python
sf_lat, sf_lon = [37.7749], [-122.4194]

print(calculate_geohashes(sf_lat, sf_lon, precision=3))  # ['9q8']
print(calculate_geohashes(sf_lat, sf_lon, precision=7))  # ['9q8yyk8']
```

## API

### `calculate_geohashes(lats, lons, precision)`

Returns a list of GeoHash strings, one for each latitude/longitude pair.

- `lats`: latitudes in decimal degrees, from -90 to 90.
- `lons`: longitudes in decimal degrees, from -180 to 180.
- `precision`: integer from 1 to 12, inclusive.

Latitude and longitude lists must have the same length. Invalid coordinates, a precision outside the supported range, or a precision that is not an integer raise `ValueError`. With valid precision, two empty lists return an empty list.

## Development

Clone the repository and install the development dependencies:

```bash
git clone https://github.com/eddiethedean/geodude.git
cd geodude
python -m pip install -e '.[dev]'
```

Run the test suite, coverage report, and code checks with:

```bash
python -m pytest
python -m pytest --cov=geodude --cov-report=html
python -m mypy src tests
python -m ruff check src tests
python -m ruff format --check src tests
```

Pytest markers are available for selecting test groups: `integration`, `performance`, and `slow`. For example, run only integration tests with `python -m pytest -m integration`.

Bug reports and contributions are welcome via [GitHub Issues](https://github.com/eddiethedean/geodude/issues) and [Pull Requests](https://github.com/eddiethedean/geodude/pulls).

## License

Geodude is released under the [MIT License](LICENSE).
