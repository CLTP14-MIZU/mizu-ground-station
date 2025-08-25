"""
Error handling module for MIZU Sensor Hub.

This module provides centralized error handling and user feedback
mechanisms for the application.
"""

from tkinter import messagebox
from typing import Optional

from config import ERROR_MESSAGES, DIALOG_TITLES


class ErrorHandler:
    """
    Centralized error handling and user feedback.

    This class provides methods for displaying error messages,
    warnings, and success messages to users in a consistent manner.
    """

    @staticmethod
    def show_configuration_error(message_key: str, **kwargs) -> None:
        """
        Show a configuration error message.

        Args:
            message_key: Key for the error message in ERROR_MESSAGES
            **kwargs: Format parameters for the message
        """
        message = ERROR_MESSAGES.get(message_key, message_key)
        if kwargs:
            message = message.format(**kwargs)

        messagebox.showerror(
            DIALOG_TITLES["configuration_error"],
            message
        )

    @staticmethod
    def show_connection_error(message_key: str, **kwargs) -> None:
        """
        Show a connection error message.

        Args:
            message_key: Key for the error message in ERROR_MESSAGES
            **kwargs: Format parameters for the message
        """
        message = ERROR_MESSAGES.get(message_key, message_key)
        if kwargs:
            message = message.format(**kwargs)

        messagebox.showerror(
            DIALOG_TITLES["connection_error"],
            message
        )

    @staticmethod
    def show_input_error(message_key: str, **kwargs) -> None:
        """
        Show an input error message.

        Args:
            message_key: Key for the error message in ERROR_MESSAGES
            **kwargs: Format parameters for the message
        """
        message = ERROR_MESSAGES.get(message_key, message_key)
        if kwargs:
            message = message.format(**kwargs)

        messagebox.showwarning(
            DIALOG_TITLES["input_error"],
            message
        )

    @staticmethod
    def show_communication_error(message_key: str, **kwargs) -> None:
        """
        Show a communication error message.

        Args:
            message_key: Key for the error message in ERROR_MESSAGES
            **kwargs: Format parameters for the message
        """
        message = ERROR_MESSAGES.get(message_key, message_key)
        if kwargs:
            message = message.format(**kwargs)

        messagebox.showerror(
            DIALOG_TITLES["communication_error"],
            message
        )

    @staticmethod
    def show_warning(title: str, message: str) -> None:
        """
        Show a warning message.

        Args:
            title: Dialog title
            message: Warning message
        """
        messagebox.showwarning(title, message)

    @staticmethod
    def show_info(title: str, message: str) -> None:
        """
        Show an information message.

        Args:
            title: Dialog title
            message: Information message
        """
        messagebox.showinfo(title, message)

    @staticmethod
    def ask_confirmation(title: str, message: str) -> bool:
        """
        Show a confirmation dialog.

        Args:
            title: Dialog title
            message: Confirmation message

        Returns:
            True if user confirms, False otherwise
        """
        return messagebox.askyesno(title, message)

    @staticmethod
    def validate_baud_rate(baud_rate_string: str) -> Optional[int]:
        """
        Validate and convert baud rate string to integer.

        Args:
            baud_rate_string: The baud rate as a string

        Returns:
            The baud rate as an integer if valid, None otherwise
        """
        try:
            baud_rate = int(baud_rate_string)
            if baud_rate <= 0:
                ErrorHandler.show_configuration_error("invalid_baud_rate")
                return None
            return baud_rate
        except ValueError:
            ErrorHandler.show_configuration_error("invalid_baud_rate")
            return None

    @staticmethod
    def validate_connection_settings(selected_os: int, selected_port: str, baud_rate_string: str) -> bool:
        """
        Validate all connection settings.

        Args:
            selected_os: Selected operating system
            selected_port: Selected port
            baud_rate_string: Baud rate as string

        Returns:
            True if all settings are valid, False otherwise
        """
        # Check if port and baud rate are provided
        if not selected_port or not baud_rate_string:
            ErrorHandler.show_configuration_error("configuration_missing")
            return False

        # Validate baud rate
        if ErrorHandler.validate_baud_rate(baud_rate_string) is None:
            return False

        # Check if OS is selected
        if selected_os not in [1, 2]:  # OS_WINDOWS, OS_LINUX
            ErrorHandler.show_configuration_error("os_not_selected")
            return False

        return True

    @staticmethod
    def handle_connection_failure(port: str, error: str) -> None:
        """
        Handle connection failure with appropriate error message.

        Args:
            port: The port that failed to connect
            error: The error message from the serial library
        """
        ErrorHandler.show_connection_error("connection_failed", port=port, error=error)

    @staticmethod
    def handle_command_validation(is_connected: bool, command_text: str) -> bool:
        """
        Validate command before sending.

        Args:
            is_connected: Whether there's an active connection
            command_text: The command text to validate

        Returns:
            True if command is valid, False otherwise
        """
        if not is_connected:
            ErrorHandler.show_input_error("no_connection")
            return False

        if not command_text:
            ErrorHandler.show_input_error("empty_command")
            return False

        return True

    @staticmethod
    def handle_send_failure(error: str) -> None:
        """
        Handle command send failure.

        Args:
            error: The error message from the serial library
        """
        ErrorHandler.show_communication_error("send_failed", error=error)
