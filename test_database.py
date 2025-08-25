#!/usr/bin/env python3
"""
Test script for MIZU Sensor Hub database functionality.

This script tests the database connection, data parsing, and storage
capabilities of the sensor hub application.
"""

import sys
from config import DATABASE_CONFIG, DATABASE_URL_TEMPLATE
from database_manager import DatabaseManager


def test_database_connection():
    """Test database connection and initialization."""
    print("Testing database connection...")

    database_url = DATABASE_URL_TEMPLATE.format(**DATABASE_CONFIG)
    db_manager = DatabaseManager(database_url)

    if db_manager.initialize():
        print("✓ Database connection successful")
        return db_manager
    else:
        print("✗ Database connection failed")
        return None


def test_data_parsing(db_manager):
    """Test sensor data parsing with various formats."""
    print("\nTesting data parsing...")

    test_cases = [
        # JSON format
        {
            "name": "JSON Format",
            "data": '{"device_id": "TEST001", "ambient_temp": 25.5, "humidity": 60.2, "soil_moisture": 45.8, "soil_temp": 22.1, "wind_speed": 5.2, "longitude": -122.4194, "latitude": 37.7749}'
        },
        # CSV format
        {
            "name": "CSV Format",
            "data": "TEST002,26.1,58.9,42.3,23.5,4.8,-122.4194,37.7749"
        },
        # Key-value format
        {
            "name": "Key-Value Format",
            "data": "device_id=TEST003,ambient_temp=24.8,humidity=62.1,soil_moisture=48.2,soil_temp=21.9,wind_speed=6.1,longitude=-122.4194,latitude=37.7749"
        },
        # Generic format (numbers only)
        {
            "name": "Generic Format",
            "data": "TEST004 27.3 55.6 39.7 24.2 3.9 -122.4194 37.7749"
        }
    ]

    for test_case in test_cases:
        print(f"\nTesting {test_case['name']}:")
        print(f"  Input: {test_case['data']}")

        # Test parsing without saving to database
        sensor_data = db_manager._parse_sensor_data(test_case['data'])

        if sensor_data:
            print(f"  ✓ Parsed successfully:")
            for key, value in sensor_data.items():
                print(f"    {key}: {value}")
        else:
            print(f"  ✗ Failed to parse")


def test_database_save(db_manager):
    """Test saving data to database."""
    print("\nTesting database save...")

    # Test data
    test_data = '{"device_id": "SAVE_TEST", "ambient_temp": 25.0, "humidity": 60.0, "soil_moisture": 45.0, "soil_temp": 22.0, "wind_speed": 5.0, "longitude": -122.4194, "latitude": 37.7749}'

    print(f"  Input: {test_data}")

    if db_manager.save_sensor_data(test_data):
        print("  ✓ Data saved to database successfully")
    else:
        print("  ✗ Failed to save data to database")


def main():
    """Main test function."""
    print("MIZU Sensor Hub Database Test")
    print("=" * 40)

    # Test database connection
    db_manager = test_database_connection()
    if not db_manager:
        print("\nCannot proceed with tests without database connection.")
        print("Please check your PostgreSQL installation and configuration.")
        return False

    # Test data parsing
    test_data_parsing(db_manager)

    # Test database save
    test_database_save(db_manager)

    print("\n" + "=" * 40)
    print("Database tests completed!")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
