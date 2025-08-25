"""
Database manager for MIZU Sensor Hub.

This module handles all database operations including retrieving sensor data
and managing database connections.
"""

from typing import Optional, List
from database_models import SensorData, get_db_session, init_database


class DatabaseManager:
    """
    Manages database operations for sensor data transmission.

    This class handles retrieving sensor data from the PostgreSQL database
    and provides methods for data transmission management.
    """

    def __init__(self, database_url: str):
        """
        Initialize the database manager.

        Args:
            database_url: SQLAlchemy database URL
        """
        self.database_url = database_url
        self._initialized = False

    def initialize(self) -> bool:
        """
        Initialize the database connection and create tables.

        Returns:
            True if initialization successful, False otherwise
        """
        try:
            init_database(self.database_url)
            self._initialized = True
            print(f"Database initialized successfully: {self.database_url}")
            return True
        except Exception as e:
            print(f"Failed to initialize database: {e}")
            return False

    def get_untransmitted_data(self) -> List[SensorData]:
        """
        Get all sensor data entries where transmitted is False.

        Returns:
            List of SensorData objects that haven't been transmitted yet
        """
        if not self._initialized:
            print("Database not initialized. Cannot retrieve data.")
            return []

        try:
            db = get_db_session()
            try:
                untransmitted_data = db.query(SensorData).filter(
                    SensorData.transmitted == False
                ).all()
                return untransmitted_data
            except Exception as e:
                print(f"Failed to retrieve untransmitted data: {e}")
                return []
            finally:
                db.close()
        except Exception as e:
            print(f"Error accessing database: {e}")
            return []

    def mark_as_transmitted(self, sensor_data_id: int) -> bool:
        """
        Mark a sensor data entry as transmitted.

        Args:
            sensor_data_id: The ID of the sensor data entry to mark as transmitted

        Returns:
            True if successfully marked, False otherwise
        """
        if not self._initialized:
            print("Database not initialized. Cannot update data.")
            return False

        try:
            db = get_db_session()
            try:
                sensor_data = db.query(SensorData).filter(
                    SensorData.id == sensor_data_id
                ).first()

                if sensor_data:
                    sensor_data.transmitted = True
                    db.commit()
                    return True
                else:
                    print(f"Sensor data with ID {sensor_data_id} not found")
                    return False
            except Exception as e:
                db.rollback()
                print(f"Failed to mark data as transmitted: {e}")
                return False
            finally:
                db.close()
        except Exception as e:
            print(f"Error accessing database: {e}")
            return False

    def format_sensor_data_for_transmission(self, sensor_data: SensorData) -> str:
        """
        Format sensor data into the required transmission format.

        Args:
            sensor_data: SensorData object to format

        Returns:
            Formatted string starting with # and ending with ~
        """
        # Format: #device_id=SENSOR001,ambient_temp=25.5,humidity=60.2,soil_moisture=45.8,soil_temp=22.1,wind_speed=5.2,longitude=-122.4194,latitude=37.7749~

        formatted_parts = [
            f"device_id={sensor_data.device_id}",
            f"ambient_temp={sensor_data.ambient_temperature or 0.0}",
            f"humidity={sensor_data.humidity or 0.0}",
            f"soil_moisture={sensor_data.soil_moisture or 0.0}",
            f"soil_temp={sensor_data.soil_temperature or 0.0}",
            f"wind_speed={sensor_data.wind_speed or 0.0}",
            f"longitude={sensor_data.longitude or 0.0}",
            f"latitude={sensor_data.latitude or 0.0}"
        ]

        return f"#{','.join(formatted_parts)}~"

    def _safe_float(self, value) -> Optional[float]:
        """Safely convert value to float."""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
