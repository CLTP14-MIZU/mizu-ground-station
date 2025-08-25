"""
Serial communication manager for MIZU Sensor Hub.

This module handles all serial port operations including connection
management, data transmission, and port discovery.
"""

import sys
import threading
from typing import List, Optional, Callable
import serial

from config import (
    SERIAL_TIMEOUT, MAX_COM_PORTS, OS_WINDOWS, OS_LINUX,
    ERROR_MESSAGES, SUCCESS_MESSAGES
)


class SerialManager:
    """
    Manages serial communication operations.

    This class handles establishing and maintaining serial connections,
    sending commands, and monitoring incoming data.
    """

    def __init__(self) -> None:
        """
        Initialize the serial manager.

        Sets up the connection state and monitoring thread.
        """
        self.serial_connection: Optional[serial.Serial] = None
        self.is_connected = False
        self.should_monitor_data = False
        self.data_monitoring_thread: Optional[threading.Thread] = None
        self.data_callback: Optional[Callable[[str], None]] = None

    def set_data_callback(self, callback: Callable[[str], None]) -> None:
        """
        Set the callback function for received data.

        Args:
            callback: Function to call when data is received
        """
        self.data_callback = callback

    def scan_available_ports(self) -> List[str]:
        """
        Scan the system for available serial ports.

        Returns:
            List of available serial port names.

        Raises:
            EnvironmentError: When running on an unsupported platform.
        """
        if sys.platform.startswith('win'):
            port_list = [f'COM{port_number + 1}' for port_number in range(MAX_COM_PORTS)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            import glob
            port_list = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            import glob
            port_list = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError(ERROR_MESSAGES["unsupported_platform"])

        available_ports = []
        for port_name in port_list:
            try:
                test_connection = serial.Serial(port_name)
                test_connection.close()
                available_ports.append(port_name)
            except (OSError, serial.SerialException):
                continue

        return available_ports

    def connect(self, port: str, baud_rate: int, os_type: int) -> bool:
        """
        Establish a serial connection.

        Args:
            port: The port to connect to
            baud_rate: The baud rate for communication
            os_type: Operating system type (OS_WINDOWS or OS_LINUX)

        Returns:
            True if connection successful, False otherwise
        """
        try:
            if os_type == OS_LINUX:
                full_port_path = f'/dev/tty{port}'
                self.serial_connection = serial.Serial(
                    full_port_path, baud_rate, timeout=SERIAL_TIMEOUT
                )
            elif os_type == OS_WINDOWS:
                self.serial_connection = serial.Serial(
                    port, baud_rate, timeout=SERIAL_TIMEOUT
                )
            else:
                return False

            self.is_connected = True
            # Disabled data monitoring for transmitter-only operation
            # self._start_data_monitoring()
            return True

        except serial.SerialException:
            self.is_connected = False
            return False

    def disconnect(self) -> None:
        """
        Close the serial connection and stop data monitoring.
        """
        self.should_monitor_data = False

        if self.serial_connection:
            try:
                self.serial_connection.close()
                print(SUCCESS_MESSAGES["connection_closed"])
            except serial.SerialException as close_error:
                print(f"Error while closing connection: {close_error}")
            finally:
                self.serial_connection = None

        self.is_connected = False

    def send_command(self, command: str, char_delay: float = 0.05) -> bool:
        """
        Send a command through the serial connection character by character.

        Args:
            command: The command string to send
            char_delay: Delay between characters in seconds (default: 0.01s = 10ms)

        Returns:
            True if command sent successfully, False otherwise
        """
        if not self.is_connected or not self.serial_connection:
            return False

        try:
            import time

            # Send each character individually with a delay
            for i, char in enumerate(command):
                self.serial_connection.write(char.encode())
                self.serial_connection.flush()  # Ensure the character is sent immediately

                # Add delay between characters
                time.sleep(char_delay)

                # Print character being sent
                print(f"{char}", end='')
            print("")
            return True
        except serial.SerialException as e:
            print(f"Error sending command: {e}")
            return False

    def _start_data_monitoring(self) -> None:
        """
        Start the data monitoring thread.
        """
        self.should_monitor_data = True
        self.data_monitoring_thread = threading.Thread(target=self._monitor_data)
        self.data_monitoring_thread.daemon = True
        self.data_monitoring_thread.start()

    def _monitor_data(self) -> None:
        """
        Monitor incoming data from the serial connection.

        This method runs in a separate thread and continuously reads
        data from the serial port, calling the data callback when
        new data is received.
        """
        while self.should_monitor_data and self.serial_connection:
            try:
                incoming_data = self.serial_connection.readline()

                if incoming_data and self.data_callback:
                    decoded_data = incoming_data.decode('utf-8', errors='ignore')
                    print(f"Received data: {decoded_data}")
                    self.data_callback(decoded_data)

            except serial.SerialException:
                break
            except UnicodeDecodeError:
                continue

    def cleanup(self) -> None:
        """
        Clean up resources before destruction.
        """
        if self.is_connected:
            self.disconnect()
