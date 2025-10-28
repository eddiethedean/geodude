# Geodude

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![GitHub](https://img.shields.io/badge/GitHub-eddiethedean%2Fgeodude-blue.svg)](https://github.com/eddiethedean/geodude)

A modern Python package for calculating GeoHash functions using PyGeodesy. Geodude provides efficient, thread-safe, cached geohash calculations for geographic coordinates with comprehensive type safety and validation.

## Features

- **🚀 Efficient Caching**: Uses `functools.lru_cache` for fast repeated calculations
- **🛡️ Input Validation**: Validates coordinate ranges and input consistency with descriptive error messages
- **📝 Type Safety**: Full type annotations with mypy validation for better IDE support and code clarity
- **🐍 Modern Python**: Supports Python 3.8+ with modern syntax and features
- **🧪 Comprehensive Testing**: 60+ tests with 100% code coverage
- **⚡ Performance**: Optimized for speed with large datasets (tested up to 10,000 coordinates)
- **🔧 Developer Experience**: Modern tooling with ruff linting/formatting and pytest

## Installation

```bash
pip install geodude
```

For development:

```bash
pip install geodude[dev]
```

## Usage

### Basic Usage

```python
from geodude import calculate_geohashes

# Calculate geohashes for multiple coordinates
lats = [37.7749, 40.7128, 51.5074]  # San Francisco, NYC, London
lons = [-122.4194, -74.0060, -0.1278]

# Calculate with 5-character precision
hashes = calculate_geohashes(lats, lons, precision=5)
print(hashes)
# Output: ['9q8yy', 'dr5rs', 'gcpvj']
```

### Single Coordinate

```python
from geodude.cluster_functions import _calculate_single_geohash

# Calculate a single geohash (cached internally)
hash_value = _calculate_single_geohash(37.7749, -122.4194, 5)
print(hash_value)  # Output: '9q8yy'
```

### Different Precision Levels

```python
# Higher precision = more specific location
lats = [37.7749]
lons = [-122.4194]

# 3-character precision (~156km accuracy)
hash_3 = calculate_geohashes(lats, lons, 3)
print(f"3-char: {hash_3[0]}")  # Output: 3-char: 9q8

# 7-character precision (~153m accuracy)  
hash_7 = calculate_geohashes(lats, lons, 7)
print(f"7-char: {hash_7[0]}")  # Output: 7-char: 9q8yyk7
```

## API Reference

### `calculate_geohashes(lats, lons, precision)`

Calculate geohashes for a list of coordinates.

**Parameters:**
- `lats` (List[float]): List of latitudes in decimal degrees (-90 to 90)
- `lons` (List[float]): List of longitudes in decimal degrees (-180 to 180)  
- `precision` (int): Geohash precision level (1 to 12)

**Returns:**
- `List[str]`: List of geohash strings

**Raises:**
- `ValueError`: If coordinates are out of valid range or lists have different lengths

**Example:**
```python
lats = [37.7749, 40.7128]
lons = [-122.4194, -74.0060]
hashes = calculate_geohashes(lats, lons, 5)
# Returns: ['9q8yy', 'dr5rs']
```

## Precision Levels

| Precision | Cell Size | Example |
|-----------|-----------|---------|
| 1 | ~5,000km × 5,000km | `9` |
| 2 | ~1,250km × 625km | `9q` |
| 3 | ~156km × 156km | `9q8` |
| 4 | ~39km × 19.5km | `9q8y` |
| 5 | ~4.9km × 4.9km | `9q8yy` |
| 6 | ~1.2km × 0.6km | `9q8yyk` |
| 7 | ~153m × 153m | `9q8yyk7` |
| 8 | ~38m × 19m | `9q8yyk7m` |
| 9 | ~4.8m × 4.8m | `9q8yyk7mg` |
| 10 | ~1.2m × 0.6m | `9q8yyk7mgp` |
| 11 | ~149mm × 149mm | `9q8yyk7mgpu` |
| 12 | ~37mm × 19mm | `9q8yyk7mgpu0` |

## Development

### Setup

```bash
git clone https://github.com/eddiethedean/geodude.git
cd geodude
pip install -e .[dev]
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=geodude --cov-report=html

# Run specific test categories
pytest -m "not slow"  # Skip slow tests
pytest -m integration  # Only integration tests
```

### Code Quality

```bash
# Type checking
mypy src tests

# Linting
ruff check src tests

# Formatting
ruff format src tests

# Auto-fix linting issues
ruff check src tests --fix
```

### Test Suite

The package includes a comprehensive test suite with:

- **60+ tests** covering all functionality
- **100% code coverage** across source files
- **Unit tests** for core functionality
- **Integration tests** for end-to-end workflows
- **Performance tests** for speed and memory efficiency
- **Edge case tests** for boundary conditions
- **Real-world scenario tests** (GPS tracking, city databases, API responses)

## License

MIT License - see [LICENSE](https://github.com/eddiethedean/geodude/blob/main/LICENSE) file for details.

## Author

Odos Matthews

## Changelog

### Version 0.1.0

**Major improvements and modernization:**

- ✅ **Modernized build system**: Migrated from setup.cfg to pyproject.toml-only (PEP 621)
- ✅ **Updated dependencies**: Latest versions of pytest, mypy, ruff, and PyGeodesy
- ✅ **Enhanced type safety**: Comprehensive type annotations with mypy validation
- ✅ **Improved caching**: Replaced global mutable cache with thread-safe `@lru_cache`
- ✅ **Input validation**: Robust coordinate and precision validation with descriptive errors
- ✅ **Comprehensive testing**: 60+ tests with 100% code coverage
- ✅ **Code quality**: Modern linting with ruff and consistent formatting
- ✅ **Performance optimization**: Tested and optimized for large datasets
- ✅ **Developer experience**: Enhanced tooling and documentation

### Version 0.0.1

- Initial release with basic geohash calculation functionality

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

- 🐛 **Report bugs**: [Create an issue](https://github.com/eddiethedean/geodude/issues)
- 💡 **Request features**: [Create an issue](https://github.com/eddiethedean/geodude/issues)
- 🔧 **Submit PRs**: [Create a pull request](https://github.com/eddiethedean/geodude/pulls)
- 📖 **View source**: [Browse the code](https://github.com/eddiethedean/geodude)

### Development Guidelines

1. **Code Style**: Follow ruff formatting and linting rules
2. **Type Safety**: Add type annotations for all new code
3. **Testing**: Maintain 100% test coverage
4. **Documentation**: Update docstrings and README as needed

### Pre-commit Checklist

- [ ] All tests pass: `pytest`
- [ ] Type checking passes: `mypy src tests`
- [ ] Linting passes: `ruff check src tests`
- [ ] Code is formatted: `ruff format src tests`
