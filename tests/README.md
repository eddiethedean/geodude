# Geodude Test Suite

This directory contains comprehensive tests for the Geodude package.

## Test Structure

- `conftest.py` - Test configuration and shared fixtures
- `test_geodude.py` - Main package tests
- `test_cluster_functions.py` - Tests for cluster_functions module
- `test_performance.py` - Performance and stress tests
- `test_utils.py` - Test utilities and helper functions
- `test_integration.py` - Integration tests
- `test_data.py` - Test data and constants
- `pytest.ini` - Pytest configuration

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test categories
```bash
# Run only unit tests
pytest -m "not slow and not integration"

# Run only integration tests
pytest -m integration

# Run only performance tests
pytest -m performance

# Skip slow tests
pytest -m "not slow"
```

### Run with coverage
```bash
pytest --cov=geodude --cov-report=html
```

### Run specific test files
```bash
pytest tests/test_geodude.py
pytest tests/test_cluster_functions.py
```

## Test Categories

### Unit Tests (`test_geodude.py`, `test_cluster_functions.py`)
- Basic functionality tests
- Input validation tests
- Error handling tests
- Caching behavior tests

### Performance Tests (`test_performance.py`)
- Performance benchmarks
- Stress tests with large datasets
- Memory usage tests
- Caching performance tests

### Integration Tests (`test_integration.py`)
- End-to-end workflow tests
- Real-world scenario simulations
- Package integration tests

### Utility Tests (`test_utils.py`)
- Test helper functions
- Edge case testing
- Boundary condition tests

## Test Data

The `test_data.py` file contains:
- Sample coordinates for testing
- Expected geohash values for known coordinates
- Test constants and fixtures

## Fixtures

Common fixtures available in `conftest.py`:
- `sample_coordinates` - Sample coordinate pairs
- `sample_coordinates_single` - Single coordinate pair
- `invalid_coordinates` - Invalid coordinates for error testing
- `mismatched_coordinates` - Mismatched length coordinates
- `empty_coordinates` - Empty coordinate lists
- `precision_levels` - Valid precision levels
- `invalid_precision_levels` - Invalid precision levels

## Coverage

The test suite aims for comprehensive coverage including:
- ✅ All public functions
- ✅ Error conditions and edge cases
- ✅ Performance characteristics
- ✅ Integration scenarios
- ✅ Caching behavior
- ✅ Input validation
- ✅ Boundary conditions
