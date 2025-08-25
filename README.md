# MIZU Sensor Hub

A modern, modular GUI application for serial communication with sensors. Built with Python and CustomTkinter, featuring a clean architecture that separates concerns and follows best design principles.

## Features

- **Serial Port Communication**: Connect to sensors via serial ports with configurable baud rates
- **Cross-Platform Support**: Works on Windows and Linux systems
- **Real-Time Data Monitoring**: View incoming sensor data in real-time
- **Command Transmission**: Send commands to connected devices
- **Database Storage**: Automatically save sensor data to PostgreSQL database with geolocation support
- **Theme Switching**: Light and dark theme support
- **Modular Architecture**: Clean, maintainable code structure
- **Error Handling**: Comprehensive error handling and user feedback

## Architecture

The application follows a modular design pattern with clear separation of concerns:

### Core Modules

- **`config.py`**: Centralized configuration management

  - Application constants and settings
  - UI configuration values
  - Error messages and dialog titles
  - Theme and color definitions

- **`serial_manager.py`**: Serial communication management

  - Port scanning and discovery
  - Connection establishment and management
  - Data transmission and reception
  - Thread-safe data monitoring

- **`ui_components.py`**: User interface components

  - `NavigationBar`: Top navigation with branding and controls
  - `ConnectionPanel`: Connection settings and configuration
  - `MainContentPanel`: Command input and data display

- **`error_handler.py`**: Centralized error handling

  - User-friendly error messages
  - Input validation
  - Consistent error reporting

- **`database_models.py`**: Database models and schema

  - SQLAlchemy model definitions
  - Database table structure
  - Connection management

- **`database_manager.py`**: Database operations

  - Sensor data parsing and storage
  - Database connection management
  - Data format handling

- **`mizu_sensor_hub.py`**: Main application orchestrator
  - Coordinates between all modules
  - Manages application lifecycle
  - Handles user interactions

## Installation

### Prerequisites

- Python 3.8 or later
- pip (Python package installer)

### Setup

1. Clone or download the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the database (see [Database Setup Guide](DATABASE_SETUP.md)):
   ```bash
   python setup_database.py
   ```

### Dependencies

- **customtkinter**: Modern GUI framework
- **pyserial**: Serial communication library
- **sqlalchemy**: Database ORM
- **psycopg2-binary**: PostgreSQL adapter
- **alembic**: Database migration tool
- **typing-extensions**: Type hints support (for Python < 3.9)

## Usage

### Running the Application

```bash
python mizu_sensor_hub.py
```

### Connecting to a Device

1. **Select Operating System**: Choose Windows or Linux
2. **Configure Baud Rate**: Enter the appropriate baud rate (default: 9600)
3. **Select Port**: Choose from available serial ports
4. **Connect**: Click the "Connect" button

### Sending Commands

1. **Ensure Connection**: Make sure you're connected to a device
2. **Enter Command**: Type your command in the input field
3. **Send**: Click "Send Command" or press Enter

### Monitoring Data

- Received data automatically appears in the display area
- Data scrolls automatically to show the latest information
- All data is logged to the console for debugging
- Sensor data is automatically saved to the PostgreSQL database

## Design Principles

### Separation of Concerns

Each module has a single, well-defined responsibility:

- **Configuration**: All settings in one place
- **Serial Communication**: Isolated from UI logic
- **UI Components**: Reusable and testable
- **Error Handling**: Centralized and consistent

### Dependency Injection

Components receive their dependencies through constructor parameters, making them:

- **Testable**: Easy to mock dependencies
- **Flexible**: Easy to swap implementations
- **Maintainable**: Clear dependency relationships

### Error Handling

Comprehensive error handling with:

- **User-Friendly Messages**: Clear, actionable error messages
- **Input Validation**: Prevents invalid operations
- **Graceful Degradation**: Application continues working when possible

### Thread Safety

- **Background Monitoring**: Serial data monitoring runs in separate thread
- **UI Updates**: Thread-safe GUI updates using `after()` method
- **Resource Management**: Proper cleanup of threads and connections

## Code Quality

### Type Hints

All functions and methods include comprehensive type hints for:

- **Parameters**: Clear input expectations
- **Return Values**: Explicit output types
- **Optional Values**: Proper handling of nullable types

### Documentation

- **Module Docstrings**: Purpose and functionality of each module
- **Class Docstrings**: Responsibilities and usage
- **Method Docstrings**: Parameters, return values, and behavior
- **Inline Comments**: Complex logic explanations

### Testing

The modular architecture makes the code highly testable:

- **Unit Tests**: Each module can be tested independently
- **Mock Dependencies**: Easy to mock serial connections and UI components
- **Integration Tests**: Test component interactions

## Extensibility

### Adding New Features

The modular design makes it easy to add new features:

1. **New UI Components**: Add to `ui_components.py`
2. **New Communication Protocols**: Extend `serial_manager.py`
3. **New Configuration Options**: Add to `config.py`
4. **New Error Types**: Extend `error_handler.py`

### Customization

- **Themes**: Add new themes in `config.py`
- **Port Scanning**: Customize port discovery logic
- **Data Processing**: Add data transformation layers
- **Logging**: Integrate with external logging systems

## Troubleshooting

### Common Issues

1. **No Ports Available**: Ensure device is connected and drivers are installed
2. **Connection Failed**: Verify baud rate and port selection
3. **Permission Errors**: Run with appropriate permissions on Linux
4. **Data Not Displaying**: Check device is sending data in expected format

### Debugging

- **Console Output**: Check console for detailed error messages
- **Port Scanning**: Verify available ports are detected
- **Connection Status**: Monitor connection state in UI

## Contributing

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions
- Include comprehensive docstrings
- Write unit tests for new features

### Architecture Guidelines

- Maintain separation of concerns
- Use dependency injection
- Keep modules focused and cohesive
- Follow the established patterns

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review the console output for error messages
3. Verify your hardware and drivers are working
4. Create an issue with detailed information about your setup

## Setting Permissions for activating virtual environment

1. Run the following command in powershell:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted