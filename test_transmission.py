"""
Test script for the transmission functionality.

This script tests the database operations and transmission formatting
to ensure everything works correctly.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database_manager import DatabaseManager
from database_models import SensorData, get_db_session
from config import DATABASE_CONFIG, DATABASE_URL_TEMPLATE


def test_database_operations():
    """Test database operations and transmission formatting."""

    # Initialize database manager
    database_url = DATABASE_URL_TEMPLATE.format(**DATABASE_CONFIG)
    db_manager = DatabaseManager(database_url)

    if not db_manager.initialize():
        print("Failed to initialize database")
        return

    print("Database initialized successfully")

    # Add some test data
    test_data = [
        {
            'device_id': 'SENSOR001',
            'ambient_temperature': 25.5,
            'humidity': 60.2,
            'soil_moisture': 45.8,
            'soil_temperature': 22.1,
            'wind_speed': 5.2,
            'longitude': -122.4194,
            'latitude': 37.7749,
            'transmitted': False
        },
        {
            'device_id': 'SENSOR002',
            'ambient_temperature': 28.3,
            'humidity': 55.7,
            'soil_moisture': 52.1,
            'soil_temperature': 24.8,
            'wind_speed': 3.8,
            'longitude': -122.4200,
            'latitude': 37.7750,
            'transmitted': False
        },
        {
            'device_id': 'SENSOR003',
            'ambient_temperature': 23.1,
            'humidity': 65.4,
            'soil_moisture': 38.9,
            'soil_temperature': 20.5,
            'wind_speed': 7.1,
            'longitude': -122.4188,
            'latitude': 37.7748,
            'transmitted': False
        }
    ]

    # Add test data to database
    db = get_db_session()
    try:
        for data in test_data:
            sensor_data = SensorData(**data)
            db.add(sensor_data)
        db.commit()
        print(f"Added {len(test_data)} test records to database")
    except Exception as e:
        db.rollback()
        print(f"Error adding test data: {e}")
    finally:
        db.close()

    # Test getting untransmitted data
    untransmitted_data = db_manager.get_untransmitted_data()
    print(f"Found {len(untransmitted_data)} untransmitted records")

    # Test formatting for transmission
    for i, sensor_data in enumerate(untransmitted_data):
        formatted = db_manager.format_sensor_data_for_transmission(sensor_data)
        print(f"Entry {i+1}: {formatted}")

    # Test marking as transmitted
    if untransmitted_data:
        first_record = untransmitted_data[0]
        if db_manager.mark_as_transmitted(first_record.id):
            print(f"Successfully marked record {first_record.id} as transmitted")
        else:
            print(f"Failed to mark record {first_record.id} as transmitted")

    # Check remaining untransmitted data
    remaining_data = db_manager.get_untransmitted_data()
    print(f"Remaining untransmitted records: {len(remaining_data)}")


if __name__ == "__main__":
    test_database_operations()
