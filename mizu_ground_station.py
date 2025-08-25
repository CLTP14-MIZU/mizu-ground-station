"""
MIZU Sensor Hub - A GUI application for transmitting sensor data from database to COM port.

This module provides a graphical user interface for connecting to COM ports
and transmitting sensor data that has been stored in the database. It supports
both Windows and Linux platforms.

The application features:
- Serial port connection management
- Database monitoring for untransmitted data
- Automatic data transmission to connected devices
- Cross-platform support (Windows/Linux)
- Light/Dark theme switching
- Real-time transmission status display
"""

import customtkinter
import threading
import time

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, DEFAULT_THEME,
    DEFAULT_COLOR_THEME, EXIT_CONFIRMATION_MESSAGE, DIALOG_TITLES,
    DATABASE_CONFIG, DATABASE_URL_TEMPLATE
)
from serial_manager import SerialManager
from ui_components import NavigationBar, ConnectionPanel, MainContentPanel
from error_handler import ErrorHandler
from database_manager import DatabaseManager


class MizuSensorHub(customtkinter.CTk):
    """
    Main application class for the MIZU Sensor Hub GUI.

    This class orchestrates the interaction between the UI components,
    serial communication manager, and error handling system.
    """

    def __init__(self) -> None:
        """
        Initialize the MIZU Sensor Hub application.

        Sets up the main window, configures appearance, initializes
        all managers and UI components, and establishes the application
        architecture.
        """
        super().__init__()

        # Configure application appearance and theme
        customtkinter.set_appearance_mode(DEFAULT_THEME)
        customtkinter.set_default_color_theme(DEFAULT_COLOR_THEME)

        # Initialize managers and handlers
        self.serial_manager = SerialManager()
        self.error_handler = ErrorHandler()

        # Initialize database manager
        database_url = DATABASE_URL_TEMPLATE.format(**DATABASE_CONFIG)
        self.database_manager = DatabaseManager(database_url)

        # Initialize database connection
        if not self.database_manager.initialize():
            print("Warning: Database initialization failed. Transmission functionality will not work.")
        else:
            print("Database initialized successfully. Ready to transmit sensor data.")

        # Setup the main application window and components
        self._configure_main_window()
        self._setup_responsive_layout()
        self._initialize_ui_components()

        # Initialize transmission loop control
        self.transmission_thread = None
        self.should_transmit = False

        # Register cleanup handler for window close events
        self.protocol("WM_DELETE_WINDOW", self._handle_window_close)

    def _start_transmission_loop(self) -> None:
        """
        Start the continuous transmission loop in a separate thread.

        This method runs continuously, checking for untransmitted data
        and sending it to the COM port.
        """
        if self.transmission_thread is None or not self.transmission_thread.is_alive():
            self.should_transmit = True
            self.transmission_thread = threading.Thread(
                target=self._transmission_loop,
                daemon=True
            )
            self.transmission_thread.start()
            print("Transmission loop started")

    def _stop_transmission_loop(self) -> None:
        """
        Stop the continuous transmission loop.
        """
        self.should_transmit = False
        print("Transmission loop stopped")

    def _transmission_loop(self) -> None:
        """
        Continuous loop that transmits untransmitted data to the COM port.

        This method runs in a separate thread and continuously:
        1. Gets all untransmitted data from the database
        2. Formats each entry into the required string format
        3. Sends the formatted string to the COM port
        4. Marks the data as transmitted
        5. Waits 5 seconds before the next iteration
        """
        while self.should_transmit:
            try:
                # Get all untransmitted data from database
                untransmitted_data = self.database_manager.get_untransmitted_data()

                if untransmitted_data:
                    self._update_transmission_status(f"Processing {len(untransmitted_data)} entries", "orange")
                    print(f"Found {len(untransmitted_data)} untransmitted data entries")
                    self._display_transmission_data(f"Starting transmission of {len(untransmitted_data)} data entries to satellite...")

                    # Process each untransmitted entry
                    for i, sensor_data in enumerate(untransmitted_data, 1):
                        try:
                            # Format the data into the required string format
                            formatted_data = self.database_manager.format_sensor_data_for_transmission(sensor_data)

                            self._update_transmission_status(f"Transmitting entry {i}/{len(untransmitted_data)}", "orange")
                            print(f"Transmitting: {formatted_data}")

                            # Display the data being uploaded in the output window
                            self._display_transmission_data(f"Uploading to satellite: {formatted_data}")

                            # Send the formatted data to COM port (similar to sending command)
                            if self.serial_manager.is_connected:
                                if self.serial_manager.send_command(formatted_data):
                                    # Mark as transmitted if send was successful
                                    if self.database_manager.mark_as_transmitted(sensor_data.id):
                                        self._update_transmission_status(f"Successfully transmitted entry {i}/{len(untransmitted_data)}", "green")
                                        print(f"Successfully transmitted and marked data ID {sensor_data.id}\n\r")
                                        self._display_transmission_data(f"✓ Successfully uploaded data ID {sensor_data.id} to satellite\n\r")
                                    else:
                                        self._update_transmission_status(f"Failed to mark entry {i} as transmitted", "red")
                                        print(f"Failed to mark data ID {sensor_data.id} as transmitted")
                                        self._display_transmission_data(f"✗ Failed to mark data ID {sensor_data.id} as transmitted")
                                else:
                                    self._update_transmission_status(f"Failed to send entry {i} to COM port", "red")
                                    print(f"Failed to send data ID {sensor_data.id} to COM port")
                                    self._display_transmission_data(f"✗ Failed to send data ID {sensor_data.id} to COM port")
                            else:
                                self._update_transmission_status("COM port not connected", "red")
                                print("COM port not connected, skipping transmission")
                                self._display_transmission_data("✗ COM port not connected - transmission skipped")

                            # Wait 5 seconds before processing next entry
                            time.sleep(5)

                        except Exception as e:
                            self._update_transmission_status(f"Error processing entry {i}: {str(e)[:50]}", "red")
                            print(f"Error processing sensor data ID {sensor_data.id}: {e}")
                            continue

                    self._update_transmission_status("All entries processed, waiting for next cycle", "green")
                    self._display_transmission_data("✓ Transmission cycle completed - waiting for next cycle...")
                else:
                    self._update_transmission_status("No untransmitted data found", "blue")
                    print("No untransmitted data found")
                    self._display_transmission_data("No untransmitted data found - waiting for new data...")

                # Wait 5 seconds before checking for new untransmitted data
                time.sleep(5)

            except Exception as e:
                self._update_transmission_status(f"Transmission loop error: {str(e)[:50]}", "red")
                print(f"Error in transmission loop: {e}")
                time.sleep(5)  # Wait before retrying

    def _update_transmission_status(self, status: str, color: str = "green") -> None:
        """
        Update the transmission status display in the UI.

        This method is thread-safe and updates the UI from the main thread.

        Args:
            status: Status message to display
            color: Color of the status text
        """
        # Use after() to update UI from main thread
        self.after(0, self.main_content_panel.update_transmission_status, status, color)

    def _display_transmission_data(self, data: str) -> None:
        """
        Display the formatted data being transmitted in the output window.

        This method is thread-safe and updates the UI from the main thread.

        Args:
            data: The formatted data string to display
        """
        self.after(0, self.main_content_panel.update_data_display, data)

    def _configure_main_window(self) -> None:
        """
        Configure the main window properties including title and size.

        Sets the window title and initial geometry based on the
        configured constants.
        """
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

    def _setup_responsive_layout(self) -> None:
        """
        Configure grid weights for responsive layout behavior.

        Sets up the grid system so that the left panel (connection settings)
        maintains a fixed width while the right panel (main content)
        expands to fill available space.
        """
        # Left panel (connection settings) - fixed width, no expansion
        self.grid_columnconfigure(0, weight=0)
        # Right panel (main content) - takes all remaining space
        self.grid_columnconfigure(1, weight=1)
        # Main content area - expands vertically
        self.grid_rowconfigure(1, weight=1)

    def _initialize_ui_components(self) -> None:
        """
        Initialize all UI components with their respective callbacks.

        Creates the navigation bar, connection panel, and main content
        panel, establishing the callback relationships between components.
        """
        # Create navigation bar with theme and close callbacks
        self.navigation_bar = NavigationBar(
            parent=self,
            theme_callback=self._switch_appearance_theme,
            close_callback=self._handle_window_close
        )

        # Create connection panel with connection and port scan callbacks
        self.connection_panel = ConnectionPanel(
            parent=self,
            connection_callback=self._toggle_serial_connection,
            port_scan_callback=self._scan_available_ports
        )

        # Create main content panel with command send callback
        self.main_content_panel = MainContentPanel(
            parent=self,
            send_command_callback=self._send_serial_command
        )

        # Set up data callback for serial manager
        self.serial_manager.set_data_callback(self._handle_received_data)

    def _switch_appearance_theme(self, selected_theme: str) -> None:
        """
        Switch the application appearance theme.

        Args:
            selected_theme: The theme to switch to ("Light" or "Dark")
        """
        customtkinter.set_appearance_mode(selected_theme)

    def _scan_available_ports(self) -> list:
        """
        Scan for available serial ports.

        Returns:
            List of available serial port names
        """
        try:
            return self.serial_manager.scan_available_ports()
        except Exception as error:
            self.error_handler.show_warning(
                "Port Scan Error",
                f"Failed to scan for available ports: {error}"
            )
            return []

    def _toggle_serial_connection(self) -> None:
        """
        Toggle the serial connection on or off.

        If currently disconnected, attempts to establish a connection.
        If currently connected, closes the existing connection.
        """
        if self.serial_manager.is_connected:
            self._close_serial_connection()
        else:
            self._establish_serial_connection()

    def _establish_serial_connection(self) -> None:
        """
        Establish a serial connection using the current settings.

        Validates user input, creates the serial connection, and updates
        the UI state accordingly.
        """
        # Get connection settings from the UI
        selected_os, selected_port, baud_rate_string = self.connection_panel.get_connection_settings()

        # Validate all connection settings
        if not self.error_handler.validate_connection_settings(selected_os, selected_port, baud_rate_string):
            return

        # Convert baud rate to integer
        baud_rate = self.error_handler.validate_baud_rate(baud_rate_string)
        if baud_rate is None:
            return

        # Attempt to establish connection
        if self.serial_manager.connect(selected_port, baud_rate, selected_os):
            # Update UI state on successful connection
            self.connection_panel.update_connection_button_state(True)
            # Start transmission loop when connection is established
            self._start_transmission_loop()
        else:
            # Handle connection failure
            self.error_handler.handle_connection_failure(selected_port, "Connection failed")

    def _close_serial_connection(self) -> None:
        """
        Close the active serial connection and update UI state.
        """
        # Stop transmission loop before disconnecting
        self._stop_transmission_loop()
        self.serial_manager.disconnect()
        self.connection_panel.update_connection_button_state(False)

    def _send_serial_command(self) -> None:
        """
        Send a command through the active serial connection.

        Validates the connection status and command input, then
        transmits the command to the connected device.
        """
        # Get command text from UI
        command_text = self.main_content_panel.get_command_text()

        # Validate command and connection
        if not self.error_handler.handle_command_validation(
            self.serial_manager.is_connected, command_text
        ):
            return

        # Send command through serial manager
        if not self.serial_manager.send_command(command_text):
            # Handle send failure
            self.error_handler.handle_send_failure("Failed to send command")
        else:
            # Clear command input on successful send
            self.main_content_panel.clear_command_input()

    def _handle_received_data(self, data: str) -> None:
        """
        Handle data received from the serial connection.

        This method is called by the serial manager when new data
        is received. It updates the UI display in a thread-safe manner.

        Args:
            data: The received data string
        """
        # Update the data display in the main thread
        self.after(0, self.main_content_panel.update_data_display, data)

    def _handle_window_close(self, event=None) -> None:
        """
        Handle the window close event.

        Ensures proper cleanup of resources before closing the application,
        including closing any active serial connections.

        Args:
            event: The window close event (optional)
        """
        # Close any active connection before exiting
        if self.serial_manager.is_connected:
            try:
                self._close_serial_connection()
            except Exception as cleanup_error:
                print(f"Error during connection cleanup: {cleanup_error}")

        # Ask user for confirmation before closing
        user_confirmation = self.error_handler.ask_confirmation(
            DIALOG_TITLES["exit_confirmation"],
            EXIT_CONFIRMATION_MESSAGE
        )

        if user_confirmation:
            self._cleanup_and_terminate()

    def _cleanup_and_terminate(self) -> None:
        """
        Perform final cleanup and terminate the application.

        Ensures all resources are properly released and the
        application is cleanly shut down.
        """
        # Clean up serial manager
        self.serial_manager.cleanup()

        # The transmission thread is a daemon thread, so it will automatically
        # terminate when the main thread ends, but we can add a flag if needed
        # in the future for more graceful shutdown

        # Destroy the main window
        self.destroy()

    def __del__(self) -> None:
        """
        Destructor to ensure cleanup when object is garbage collected.

        Provides a safety net to ensure resources are properly
        released even if the object is not explicitly destroyed.
        """
        try:
            if hasattr(self, 'serial_manager'):
                self.serial_manager.cleanup()
        except Exception:
            # Ignore errors during cleanup in destructor
            pass


def main() -> None:
    """
    Main entry point for the MIZU Sensor Hub application.

    Creates and starts the main application window, beginning
    the event loop that handles user interactions.
    """
    # Create the main application instance
    sensor_hub_app = MizuSensorHub()

    # Start the main event loop
    sensor_hub_app.mainloop()


if __name__ == "__main__":
    main()