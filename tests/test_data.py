"""Test data and fixtures for Geodude package tests."""

# This file can be used to store test data, sample files, or other test resources
# For now, it's empty but can be expanded as needed

# Example test data structures:
SAMPLE_COORDINATES = [
    (37.7749, -122.4194),  # San Francisco
    (40.7128, -74.0060),  # New York
    (51.5074, -0.1278),  # London
    (35.6762, 139.6503),  # Tokyo
    (-33.8688, 151.2093),  # Sydney
]

EXPECTED_GEOHASHES_SF = {
    1: "9",
    2: "9q",
    3: "9q8",
    4: "9q8y",
    5: "9q8yy",
    6: "9q8yyk",
    7: "9q8yyk7",
    8: "9q8yyk7m",
}

EXPECTED_GEOHASHES_NY = {
    1: "d",
    2: "dr",
    3: "dr5",
    4: "dr5r",
    5: "dr5rs",
    6: "dr5rsj",
    7: "dr5rsjz",
    8: "dr5rsjzq",
}
