# Test Data Directory

This directory contains test data files and resources for the Geodude test suite.

## Contents

- `sample_coordinates.json` - Sample coordinate data in JSON format
- `expected_geohashes.json` - Expected geohash results for known coordinates
- `performance_data.csv` - Large datasets for performance testing

## Usage

Test data files can be loaded in tests using:

```python
import json
from pathlib import Path

def load_test_data(filename):
    data_dir = Path(__file__).parent / "data"
    with open(data_dir / filename) as f:
        return json.load(f)
```
