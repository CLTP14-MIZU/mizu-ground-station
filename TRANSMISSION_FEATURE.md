# Transmission Feature Documentation

## Overview

The MIZU Ground Station application is designed to continuously monitor the database for untransmitted sensor data and send it to connected devices via the COM port. This application acts as a data transmitter that reads from the database and uploads data to external devices.

## How It Works

### 1. Database Monitoring

- The application connects to the PostgreSQL database on startup
- A background thread continuously queries the database for records where `transmitted = false`
- This monitoring runs every 5 seconds

### 2. Data Formatting

- Each untransmitted record is formatted into a specific string format:
  ```
  #device_id=SENSOR001,ambient_temp=25.5,humidity=60.2,soil_moisture=45.8,soil_temp=22.1,wind_speed=5.2,longitude=-122.4194,latitude=37.7749~
  ```
- The format starts with `#` and ends with `~`
- All sensor values are included in key=value pairs separated by commas

### 3. Transmission Process

- For each untransmitted record:
  1. Format the data into the required string format
  2. Send the formatted string to the COM port (same as the "Send Command" functionality)
  3. If transmission is successful, mark the record as `transmitted = true` in the database
  4. Wait 5 seconds before processing the next record

### 4. Status Display

- The UI includes a transmission status display that shows:
  - Current transmission status
  - Number of entries being processed
  - Success/failure messages
  - Error information

## Features Preserved

All existing functionality remains unchanged:

- ✅ COM port connection management
- ✅ Dark/Light mode switching
- ✅ Windows/Linux platform selection
- ✅ Manual command sending
- ✅ Real-time data display

## Important Note

This application is designed to **read from the database and upload data** only. It does not:

- Receive sensor data from COM ports
- Save incoming sensor data to the database
- Parse or process incoming sensor data

The application expects that sensor data has already been stored in the database by other means (e.g., another application or data collection system).

## Database Schema

The transmission feature uses the existing `mizu_sensor_hub` table with the following key fields:

```sql
CREATE TABLE mizu_sensor_hub (
    id SERIAL PRIMARY KEY,
    device_id VARCHAR(100) NOT NULL,
    ambient_temperature FLOAT,
    humidity FLOAT,
    soil_moisture FLOAT,
    soil_temperature FLOAT,
    wind_speed FLOAT,
    longitude FLOAT,
    latitude FLOAT,
    transmitted BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

## Usage

### Starting the Application

1. Run the main application: `python mizu_ground_station.py`
2. The transmission loop starts automatically in the background
3. Connect to a COM port as usual
4. The transmission process will begin automatically

### Monitoring Transmission

- Watch the "Transmission Status" display in the main window
- Check the console output for detailed transmission logs
- The status will show:
  - "Ready" - System is ready
  - "Processing X entries" - Currently processing data
  - "Transmitting entry X/Y" - Sending specific entry
  - "Successfully transmitted entry X/Y" - Transmission successful
  - "COM port not connected" - No active connection
  - Error messages for any issues

### Testing the Feature

1. Add test data to the database using your preferred method:
   - Direct database insertion
   - Another application that saves sensor data
   - Database management tools
   - Or run the test script: `python test_transmission.py`
2. This will add 3 test records to the database
3. Start the main application and connect to a COM port
4. Watch the transmission process in action

## Data Requirements

The application expects sensor data to be present in the database with the following structure:

- `device_id`: String identifier for the sensor
- `ambient_temperature`: Float value for ambient temperature
- `humidity`: Float value for humidity percentage
- `soil_moisture`: Float value for soil moisture percentage
- `soil_temperature`: Float value for soil temperature
- `wind_speed`: Float value for wind speed
- `longitude`: Float value for GPS longitude
- `latitude`: Float value for GPS latitude
- `transmitted`: Boolean flag (should be `false` for untransmitted data)
- `timestamp`: Timestamp when the data was recorded

## Error Handling

The transmission loop includes comprehensive error handling:

- Database connection errors
- COM port communication failures
- Data formatting errors
- Individual record processing failures

All errors are logged to the console and displayed in the UI status.

## Configuration

The transmission timing can be adjusted by modifying the `time.sleep(5)` calls in the `_transmission_loop` method in `mizu_ground_station.py`:

- First sleep: Time between processing each record (currently 5 seconds)
- Second sleep: Time between checking for new untransmitted data (currently 5 seconds)

## Thread Safety

The transmission loop runs in a daemon thread, which means:

- It will automatically terminate when the main application closes
- UI updates are performed thread-safely using `self.after(0, ...)`
- Database operations are properly handled with session management

## Troubleshooting

### Common Issues

1. **No transmission happening**

   - Check if COM port is connected
   - Verify database connection
   - Look for untransmitted records in database

2. **Transmission failures**

   - Check COM port connection status
   - Verify device is ready to receive data
   - Check console for error messages

3. **Database errors**
   - Verify database configuration in `config.py`
   - Check database server is running
   - Ensure proper permissions

### Debug Information

- All transmission activities are logged to the console
- Status updates are shown in the UI
- Database operations include error logging
