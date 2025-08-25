"""
UI Components module for MIZU Ground Station.

This module contains all GUI widget creation and management logic,
separated from the main application logic for better maintainability.
"""

import tkinter as tk
from tkinter import END, VERTICAL
import customtkinter

from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, DEFAULT_THEME,
    DEFAULT_COLOR_THEME, DEFAULT_FONT, DEFAULT_FONT_SIZE,
    TITLE_FONT, TITLE_FONT_SIZE, ICON_FONT, ICON_FONT_SIZE,
    ICON_COLOR, TITLE_COLOR, THEME_OPTIONS, OS_WINDOWS, OS_LINUX,
    DEFAULT_BAUD_RATE
)


class NavigationBar:
    """Manages the top navigation bar with branding and controls."""

    def __init__(self, parent, theme_callback, close_callback):
        """
        Initialize the navigation bar.

        Args:
            parent: Parent widget
            theme_callback: Callback for theme changes
            close_callback: Callback for close button
        """
        self.parent = parent
        self.theme_callback = theme_callback
        self.close_callback = close_callback
        self._create_navigation_bar()

    def _create_navigation_bar(self):
        """Create the navigation bar with all its components."""
        # Create the main navigation bar container
        self.navigation_bar = customtkinter.CTkFrame(
            master=self.parent, height=50, corner_radius=5
        )
        self.navigation_bar.grid(
            row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=(10, 5)
        )

        # Configure grid columns for proper element distribution
        self.navigation_bar.grid_columnconfigure(0, weight=0)  # Icon - fixed width
        self.navigation_bar.grid_columnconfigure(1, weight=1)  # Title - expands
        self.navigation_bar.grid_columnconfigure(2, weight=0)  # Theme selector - fixed
        self.navigation_bar.grid_columnconfigure(3, weight=0)  # Close button - fixed

        self._create_app_icon()
        self._create_app_title()
        self._create_theme_selector()
        self._create_close_button()

    def _create_app_icon(self):
        """Create the application icon with satellite dish emoji."""
        self.app_icon_label = customtkinter.CTkLabel(
            master=self.navigation_bar,
            text="🛰️",
            font=(ICON_FONT, ICON_FONT_SIZE, "bold"),
            text_color=ICON_COLOR
        )
        self.app_icon_label.grid(row=0, column=0, pady=10, padx=(10, 5), sticky="w")

    def _create_app_title(self):
        """Create the application title."""
        self.app_title_label = customtkinter.CTkLabel(
            master=self.navigation_bar,
            text=WINDOW_TITLE,
            font=(TITLE_FONT, TITLE_FONT_SIZE, "bold"),
            text_color=TITLE_COLOR
        )
        self.app_title_label.grid(row=0, column=1, pady=10, padx=(10, 10), sticky="w")

    def _create_theme_selector(self):
        """Create the theme selection dropdown."""
        self.theme_selector = customtkinter.CTkOptionMenu(
            master=self.navigation_bar,
            values=THEME_OPTIONS,
            command=self.theme_callback,
            width=100
        )
        self.theme_selector.grid(row=0, column=2, pady=10, padx=10, sticky="e")

    def _create_close_button(self):
        """Create the close application button."""
        self.close_app_button = customtkinter.CTkButton(
            master=self.navigation_bar,
            text="Close",
            command=self.close_callback,
            width=80
        )
        self.close_app_button.grid(row=0, column=3, pady=10, padx=10, sticky="e")


class ConnectionPanel:
    """Manages the connection settings panel."""

    def __init__(self, parent, connection_callback, port_scan_callback):
        """
        Initialize the connection panel.

        Args:
            parent: Parent widget
            connection_callback: Callback for connection toggle
            port_scan_callback: Callback to scan for available ports
        """
        self.parent = parent
        self.connection_callback = connection_callback
        self.port_scan_callback = port_scan_callback
        self._create_connection_panel()

    def _create_connection_panel(self):
        """Create the connection settings panel with all components."""
        # Create the main connection settings container
        self.connection_settings_panel = customtkinter.CTkFrame(
            master=self.parent, corner_radius=5
        )
        self.connection_settings_panel.grid(row=1, column=0, sticky="nsw", padx=10, pady=10)

        self._create_os_selection_section()
        self._create_serial_configuration_section()

    def _create_os_selection_section(self):
        """Create the operating system selection section."""
        # Create container for OS selection
        self.os_selection_frame = customtkinter.CTkFrame(
            master=self.connection_settings_panel, height=60, corner_radius=5
        )
        self.os_selection_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        self.os_selection_frame.grid_columnconfigure(0, weight=1)
        self.os_selection_frame.grid_columnconfigure(1, weight=1)

        # Create radio button variable to track selection
        self.selected_os = tk.IntVar()

        # Create Windows radio button
        self.windows_os_radio = customtkinter.CTkRadioButton(
            master=self.os_selection_frame,
            variable=self.selected_os,
            value=OS_WINDOWS,
            text="Windows"
        )
        self.windows_os_radio.grid(row=0, column=0, pady=10, padx=20, sticky="ew")

        # Create Linux radio button
        self.linux_os_radio = customtkinter.CTkRadioButton(
            master=self.os_selection_frame,
            variable=self.selected_os,
            value=OS_LINUX,
            text="Linux"
        )
        self.linux_os_radio.grid(row=0, column=1, pady=10, padx=20, sticky="ew")

        # Set Windows as default selection
        self.selected_os.set(OS_WINDOWS)

    def _create_serial_configuration_section(self):
        """Create the serial port configuration section."""
        # Create container for serial settings
        self.serial_settings_frame = customtkinter.CTkFrame(
            master=self.connection_settings_panel, corner_radius=5
        )
        self.serial_settings_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")
        self.serial_settings_frame.grid_columnconfigure(1, weight=1)

        self._create_baud_rate_configuration()
        self._create_port_selection_configuration()
        self._create_connection_control_button()

    def _create_baud_rate_configuration(self):
        """Create the baud rate input field and label."""
        # Create baud rate label
        self.baud_rate_label = customtkinter.CTkLabel(
            master=self.serial_settings_frame,
            height=30,
            text="Baud Rate",
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        )
        self.baud_rate_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        # Create baud rate input field
        self.baud_rate_input = customtkinter.CTkEntry(
            master=self.serial_settings_frame, width=120, height=30
        )
        self.baud_rate_input.insert(0, DEFAULT_BAUD_RATE)
        self.baud_rate_input.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

    def _create_port_selection_configuration(self):
        """Create the serial port selection dropdown and label."""
        # Create port selection label
        self.port_selection_label = customtkinter.CTkLabel(
            master=self.serial_settings_frame,
            height=30,
            text="PORT",
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE)
        )
        self.port_selection_label.grid(row=1, column=0, pady=10, padx=10, sticky="w")

        # Get available serial ports and create dropdown
        available_serial_ports = self.port_scan_callback()
        self.port_selection_dropdown = customtkinter.CTkOptionMenu(
            master=self.serial_settings_frame,
            width=120,
            height=30,
            values=available_serial_ports
        )
        self.port_selection_dropdown.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

    def _create_connection_control_button(self):
        """Create the main connection control button."""
        self.connection_control_button = customtkinter.CTkButton(
            master=self.serial_settings_frame,
            height=35,
            text="Connect and Send",
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),
            command=self.connection_callback
        )
        self.connection_control_button.grid(
            row=2, column=0, columnspan=2, pady=10, padx=10, sticky="ew"
        )

    def update_connection_button_state(self, is_connected: bool):
        """
        Update the connection button text and state.

        Args:
            is_connected: Current connection status
        """
        if is_connected:
            self.connection_control_button.configure(text="Disconnect", state="normal")
        else:
            self.connection_control_button.configure(text="Connect and Send", state="normal")

    def get_connection_settings(self):
        """
        Get the current connection settings.

        Returns:
            Tuple of (selected_os, selected_port, baud_rate)
        """
        return (
            self.selected_os.get(),
            self.port_selection_dropdown.get(),
            self.baud_rate_input.get()
        )


class MainContentPanel:
    """Manages the main content panel for command input and data display."""

    def __init__(self, parent, send_command_callback):
        """
        Initialize the main content panel.

        Args:
            parent: Parent widget
            send_command_callback: Callback for sending commands
        """
        self.parent = parent
        self.send_command_callback = send_command_callback
        self._create_main_content_panel()

    def _create_main_content_panel(self):
        """Create the main content panel with all components."""
        # Create the main content container
        self.main_content_panel = customtkinter.CTkFrame(master=self.parent, corner_radius=5)
        self.main_content_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.main_content_panel.grid_columnconfigure(0, weight=1)
        self.main_content_panel.grid_rowconfigure(2, weight=1)  # Changed from 1 to 2 to accommodate status

        self._create_command_input_section()
        self._create_transmission_status_section()
        self._create_data_display_section()

    def _create_command_input_section(self):
        """Create the command input section with text field and send button."""
        # Create container for command input
        self.command_input_frame = customtkinter.CTkFrame(
            master=self.main_content_panel, height=60, corner_radius=5
        )
        self.command_input_frame.grid(row=0, column=0, pady=10, padx=10, sticky="ew")
        self.command_input_frame.grid_columnconfigure(0, weight=1)

        # Create command input text field
        self.command_input_field = customtkinter.CTkEntry(
            master=self.command_input_frame, height=35
        )
        self.command_input_field.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        # Create send command button
        self.send_command_button = customtkinter.CTkButton(
            master=self.command_input_frame,
            width=120,
            height=35,
            text="Send Command",
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),
            command=self.send_command_callback
        )
        self.send_command_button.grid(row=0, column=1, pady=10, padx=10, sticky="e")

    def _create_transmission_status_section(self):
        """Create the transmission status display section."""
        # Create container for transmission status
        self.transmission_status_frame = customtkinter.CTkFrame(
            master=self.main_content_panel, height=40, corner_radius=5
        )
        self.transmission_status_frame.grid(row=1, column=0, pady=(5, 10), padx=10, sticky="ew")
        self.transmission_status_frame.grid_columnconfigure(0, weight=1)

        # Create status label
        self.transmission_status_label = customtkinter.CTkLabel(
            master=self.transmission_status_frame,
            text="Transmission Status: Ready",
            font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),
            text_color="green"
        )
        self.transmission_status_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    def update_transmission_status(self, status: str, color: str = "green"):
        """
        Update the transmission status display.

        Args:
            status: Status message to display
            color: Color of the status text (green, orange, red, etc.)
        """
        self.transmission_status_label.configure(text=f"Transmission Status: {status}", text_color=color)

    def _create_data_display_section(self):
        """Create the data display section with text area and scrollbar."""
        # Create container for data display
        self.data_display_frame = customtkinter.CTkFrame(
            master=self.main_content_panel, corner_radius=5
        )
        self.data_display_frame.grid(row=1, column=0, pady=10, padx=10, sticky="nsew")
        self.data_display_frame.grid_columnconfigure(0, weight=1)
        self.data_display_frame.grid_rowconfigure(0, weight=1)

        # Create text area for displaying received data
        self.data_display_text_area = tk.Text(
            self.data_display_frame,
            font=(DEFAULT_FONT, 12),
            padx=15,
            pady=10
        )

        # Create vertical scrollbar for the text area
        self.data_display_scrollbar = tk.Scrollbar(
            self.data_display_frame,
            orient=VERTICAL,
            command=self.data_display_text_area.yview
        )

        # Configure text area to use the scrollbar
        self.data_display_text_area.configure(yscrollcommand=self.data_display_scrollbar.set)

        # Position the text area and scrollbar in the frame
        self.data_display_text_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.data_display_scrollbar.grid(row=0, column=1, sticky="ns", pady=10)

    def get_command_text(self) -> str:
        """
        Get the current command text from the input field.

        Returns:
            The command text string
        """
        return self.command_input_field.get().strip()

    def clear_command_input(self):
        """Clear the command input field."""
        self.command_input_field.delete(0, END)

    def update_data_display(self, data: str):
        """
        Update the data display area with new data.

        Args:
            data: The data string to display
        """
        # Add a newline before the new data to separate it from previous entries
        self.data_display_text_area.insert(END, data + "\n")
        self.data_display_text_area.see(END)  # Auto-scroll to show latest data
