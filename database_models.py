"""
Database models for MIZU Sensor Hub.

This module defines the SQLAlchemy models for storing sensor data
in the PostgreSQL database.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class SensorData(Base):
    """
    Model for storing sensor data in the database.

    This table stores all sensor readings including device ID,
    environmental measurements, geolocation, and transmission status.
    """
    __tablename__ = 'mizu_sensor_hub'

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(String(100), nullable=False, index=True)
    ambient_temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    soil_moisture = Column(Float, nullable=True)
    soil_temperature = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    transmitted = Column(Boolean, default=False, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f"<SensorData(device_id='{self.device_id}', timestamp='{self.timestamp}')>"


# Database engine and session factory
engine = None
SessionLocal = None


def init_database(database_url: str):
    """
    Initialize the database connection and create tables.

    Args:
        database_url: SQLAlchemy database URL (e.g., postgresql://user:pass@localhost/mizu_sensor_hub)
    """
    global engine, SessionLocal

    engine = create_engine(database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)


def get_db_session():
    """
    Get a database session.

    Returns:
        Database session instance
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")

    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise
