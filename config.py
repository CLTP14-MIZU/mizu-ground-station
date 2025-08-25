"""
Configuration module for MIZU Ground Station.

This module contains all application constants, configuration settings,
and default values used throughout the application.
"""

# Application window configuration
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
WINDOW_TITLE = "MIZU Satellite Uplink"

# Serial communication configuration
DEFAULT_BAUD_RATE = "9600"
SERIAL_TIMEOUT = 0.1
MAX_COM_PORTS = 256

# UI Configuration
DEFAULT_THEME = "Light"
DEFAULT_COLOR_THEME = "blue"
DEFAULT_FONT = "Roboto Medium"
DEFAULT_FONT_SIZE = 14
TITLE_FONT = "Roboto"
TITLE_FONT_SIZE = 22
ICON_FONT = "Segoe UI Emoji"
ICON_FONT_SIZE = 28

# Colors
ICON_COLOR = "#006400"  # Dark green
TITLE_COLOR = "#1f538d"  # Blue

# Operating system values
OS_WINDOWS = 1
OS_LINUX = 2

# Theme options
THEME_OPTIONS = ["Light", "Dark"]

# Error messages
ERROR_MESSAGES = {
    "configuration_missing": "Please specify both port and baud rate before connecting",
    "invalid_baud_rate": "Baud rate must be a valid number",
    "os_not_selected": "Please select an operating system before connecting",
    "connection_failed": "Failed to connect to {port}: {error}",
    "no_connection": "No active connection. Please connect to a device first.",
    "empty_command": "Please enter a command to send",
    "send_failed": "Failed to send command: {error}",
    "unsupported_platform": "Unsupported platform detected"
}

# Success messages
SUCCESS_MESSAGES = {
    "connection_closed": "Serial connection successfully closed",
    "command_sent": "Command sent successfully: {command}"
}

# Dialog titles
DIALOG_TITLES = {
    "configuration_error": "Configuration Error",
    "connection_error": "Connection Error",
    "input_error": "Input Error",
    "communication_error": "Communication Error",
    "exit_confirmation": "Exit Application"
}

# Database configuration
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "mizu_sensor_hub",
    "username": "postgres",
    "password": "deepsynopsis"
}

# Database URL template
DATABASE_URL_TEMPLATE = "postgresql://{username}:{password}@{host}:{port}/{database}"

# Exit confirmation message
EXIT_CONFIRMATION_MESSAGE = "Are you sure you want to exit the MIZU Ground Station?"
