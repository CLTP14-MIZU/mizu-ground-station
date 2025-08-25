# MIZU Sensor Hub Database Setup Guide

This guide will help you set up the PostgreSQL database for the MIZU Sensor Hub application to store sensor data.

## Prerequisites

1. **PostgreSQL Installation**

   - Download and install PostgreSQL from [https://www.postgresql.org/download/](https://www.postgresql.org/download/)
   - Ensure `psql` command-line tool is available in your PATH
   - Note down your PostgreSQL username and password

2. **Python Dependencies**
   - Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Database Configuration

The database configuration is defined in `config.py`. You can modify these settings:

```python
DATABASE_CONFIG = {
    "host": "localhost",        # PostgreSQL server host
    "port": 5432,              # PostgreSQL port
    "database": "mizu_sensor_hub",  # Database name
    "username": "postgres",     # PostgreSQL username
    "password": "password"      # PostgreSQL password
}
```

**Important**: Update the username and password to match your PostgreSQL installation.

## Quick Setup

### Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
python setup_database.py
```

This script will:

1. Check if PostgreSQL is installed
2. Create the database if it doesn't exist
3. Run database migrations to create tables
4. Test the database connection

### Option 2: Manual Setup

If you prefer to set up the database manually:

1. **Create the database:**

   ```bash
   psql -U postgres -c "CREATE DATABASE mizu_sensor_hub;"
   ```

2. **Update alembic.ini:**
   Edit `alembic.ini` and update the database URL:

   ```ini
   sqlalchemy.url = postgresql://username:password@localhost/mizu_sensor_hub
   ```

3. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

## Database Schema

The application creates a single table `mizu_sensor_hub` with the following columns:

| Column              | Type        | Description                          |
| ------------------- | ----------- | ------------------------------------ |
| id                  | Integer     | Primary key (auto-increment)         |
| device_id           | String(100) | Device identifier                    |
| ambient_temperature | Float       | Ambient temperature reading          |
| humidity            | Float       | Humidity percentage                  |
| soil_moisture       | Float       | Soil moisture level                  |
| soil_temperature    | Float       | Soil temperature reading             |
| wind_speed          | Float       | Wind speed measurement               |
| longitude           | Float       | Geographic longitude coordinate      |
| latitude            | Float       | Geographic latitude coordinate       |
| transmitted         | Boolean     | Transmission status (default: false) |
| timestamp           | DateTime    | Record creation timestamp            |

## Sensor Data Format

The application can parse sensor data in various formats:

### JSON Format

```json
{
  "device_id": "SENSOR001",
  "ambient_temp": 25.5,
  "humidity": 60.2,
  "soil_moisture": 45.8,
  "soil_temp": 22.1,
  "wind_speed": 5.2,
  "longitude": -122.4194,
  "latitude": 37.7749
}
```

### CSV Format

```
SENSOR001,25.5,60.2,45.8,22.1,5.2,-122.4194,37.7749
```

### Key-Value Format

```
device_id=SENSOR001,ambient_temp=25.5,humidity=60.2,soil_moisture=45.8,soil_temp=22.1,wind_speed=5.2,longitude=-122.4194,latitude=37.7749
```

## Running the Application

After setting up the database:

1. **Start the application:**

   ```bash
   python mizu_sensor_hub.py
   ```

2. **Connect to your sensor device** using the GUI

3. **Monitor sensor data** - Data will be automatically saved to the database

## Troubleshooting

### Database Connection Issues

1. **Check PostgreSQL service:**

   - Windows: Check Services app for "PostgreSQL" service
   - Linux: `sudo systemctl status postgresql`

2. **Verify credentials:**

   - Test connection: `psql -U username -d mizu_sensor_hub`
   - Update `config.py` with correct credentials

3. **Check firewall settings:**
   - Ensure PostgreSQL port (5432) is not blocked

### Migration Issues

1. **Reset migrations:**

   ```bash
   alembic downgrade base
   alembic upgrade head
   ```

2. **Check database URL:**
   - Verify the URL in `alembic.ini` matches your configuration

### Data Parsing Issues

If sensor data is not being saved:

1. **Check data format** - Ensure your sensor sends data in one of the supported formats
2. **Review console output** - The application prints parsing attempts
3. **Customize parsing** - Modify `database_manager.py` to match your sensor's data format

## Database Management

### Viewing Data

Connect to the database and query the table:

```sql
-- Connect to database
psql -U username -d mizu_sensor_hub

-- View recent data
SELECT * FROM mizu_sensor_hub ORDER BY timestamp DESC LIMIT 10;

-- Count total records
SELECT COUNT(*) FROM mizu_sensor_hub;

-- View data by device
SELECT * FROM mizu_sensor_hub WHERE device_id = 'SENSOR001';
```

### Backup and Restore

```bash
# Backup
pg_dump -U username mizu_sensor_hub > backup.sql

# Restore
psql -U username mizu_sensor_hub < backup.sql
```

## Support

If you encounter issues:

1. Check the console output for error messages
2. Verify PostgreSQL installation and configuration
3. Ensure all Python dependencies are installed
4. Review the database connection settings in `config.py`
