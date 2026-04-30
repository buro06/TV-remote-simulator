"""
Loads the Qt  .ui file, connects all controls, and keeps the display synchronized with TV state.
"""

import os
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import *
from gui import Television


class Logic(QMainWindow):
    """
    Main application window for the Smart TV Remote.

    Loads the UI layout from QT file
    """

    def __init__(self) -> None:
        """Initialize the window, load the .ui file, and set up the TV."""
        super().__init__()

        # I am using the uic here to make it easier so I don't have to export/build the .ui file every time I update it.
        # AI helped here in this boilerplate to load the ui file from Qt designer
        ui_path = os.path.join(os.path.dirname(__file__), "ui", "television.ui")
        uic.loadUi(ui_path, self)

        self._tv: Television = Television()

        self._connectInputs()
        self._update_display()
        self.setFixedSize(400, 750)

    #setup handlers

    def _connectInputs(self) -> None:
        """Connect each buttons clicked event to its appropriate function."""
        self.btn_power.clicked.connect(self._on_power)
        self.btn_mute.clicked.connect(self._on_mute)
        self.btn_ch_up.clicked.connect(self._on_ch_up)
        self.btn_ch_down.clicked.connect(self._on_ch_down)
        self.btn_vol_up.clicked.connect(self._on_vol_up)
        self.btn_vol_down.clicked.connect(self._on_vol_down)
        self.btn_go_channel.clicked.connect(self._on_go_channel)

    #display update functions

    def _update_display(self) -> None:
        """Refresh all labels and the favorites list to match current TV state.
            Will be run usually after an event happens
            """
        self._update_channel_image()

        if self._tv.is_on():
            self.label_power_status.setText("POWER: ON")
            self.label_channel_display.setText(f"CH: {self._tv.get_channel()}")
            display_vol = 0 if self._tv.is_muted() else self._tv.get_volume()
            self.label_volume_display.setText(f"VOL: {display_vol} / {Television.MAX_VOLUME}")
            self.btn_vol_up.setEnabled(True)
            self.btn_vol_down.setEnabled(True)
            self.btn_ch_up.setEnabled(True)
            self.btn_ch_down.setEnabled(True)
            if self._tv.is_muted():
                self.label_mute_display.setText("[ MUTED ]")
            else:
                self.label_mute_display.setText("")

        else:
            self.label_power_status.setText("POWER: OFF")
            self.btn_vol_up.setEnabled(False)
            self.btn_vol_down.setEnabled(False)
            self.btn_ch_up.setEnabled(False)
            self.btn_ch_down.setEnabled(False)
            self.label_channel_display.setText("CH: --")
            self.label_volume_display.setText("VOL: --")
            self.label_mute_display.setText("")

    def _update_channel_image(self) -> None:
        """Load and display the image for the current channel, or nothing if none exists."""
        if not self._tv.is_on():
            self.label_channel_image.clear()
            return

        channel = self._tv.get_channel()
        image_path = os.path.join(os.path.dirname(__file__), "images", f"{channel}.png")

        if os.path.isfile(image_path):
            # AI helped here with adding the image and scaling it to fill the box.
            pixmap = QPixmap(image_path).scaled(
                self.label_channel_image.width(),
                self.label_channel_image.height()
            )
            self.label_channel_image.setPixmap(pixmap)
        else:
            self.label_channel_image.clear()

    def _set_status(self, message: str) -> None:
        """Use this function to show a temporary status in the area at the bottom
        of the screen. Shows for 3 seconds

        Args: text, string, what to be displayed on the GUI message box:
         Return nothing """
        self.statusbar.showMessage(message, 3000)

    #handle button press events

    def _on_power(self) -> None:
        """Toggle TV power and refresh the display."""
        try:
            self._tv.power()
            state = "ON" if self._tv.is_on() else "OFF"
            self._set_status(f"TV turned {state}.")
            self._update_display()
        except Exception as err:
            QMessageBox.critical(self, "Error", f"Power failed: {err}")

    def _on_mute(self) -> None:
        """Toggle mute and refresh the display."""
        try:
            self._tv.mute()
            if self._tv.is_on():
                self._set_status("Muted." if self._tv.is_muted() else "Unmuted.")
            else:
                self._set_status("TV is off.")
            self._update_display()
        except Exception as err:
            QMessageBox.critical(self, "Error", f"Mute failed: {err}")

    def _on_ch_up(self) -> None:
        """Increase channel by 1 and refresh the display."""
        try:
            self._tv.channel_up()
            if self._tv.is_on():
                self._set_status(f"Channel -> {self._tv.get_channel()}")
            self._update_display()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Channel up failed: {e}")

    def _on_ch_down(self) -> None:
        """Decrease channel by 1 and refresh the display."""
        try:
            self._tv.channel_down()
            if self._tv.is_on():
                self._set_status(f"Channel -> {self._tv.get_channel()}")
            self._update_display()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Channel down failed: {e}")

    def _on_vol_up(self) -> None:
        """Increase volume by 1 and refresh the display."""
        try:
            self._tv.volume_up()
            if self._tv.is_on():
                self._set_status(f"Volume -> {self._tv.get_volume()}")
            self._update_display()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Volume up failed: {e}")

    def _on_vol_down(self) -> None:
        """Decrease volume by 1 and refresh the display."""
        try:
            self._tv.volume_down()
            if self._tv.is_on():
                self._set_status(f"Volume -> {self._tv.get_volume()}")
            self._update_display()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Volume down failed: {e}")

    def _on_go_channel(self) -> None:
        """Read the direct channel input and go to that channel."""
        try:
            raw: str = self.input_channel.text().strip()

            if not raw:
                self._set_status("Enter a channel number first.")
                return

            channel: int = int(raw)

            if not (Television.MIN_CHANNEL <= channel <= Television.MAX_CHANNEL):
                QMessageBox.warning(
                    self, "Invalid Channel",
                    f"Channel must be between {Television.MIN_CHANNEL} and {Television.MAX_CHANNEL}."
                )
                return

            if self._tv.set_channel(channel):
                self._set_status(f"Jumped to channel {channel}.")
            else:
                self._set_status("TV is off, cannot change channel.")

            self.input_channel.clear()
            self._update_display()

        except ValueError:
            QMessageBox.warning(
                self, "Invalid Input",
                "Please enter a whole number between 1 and 20"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Channel navigation failed: {e}")
