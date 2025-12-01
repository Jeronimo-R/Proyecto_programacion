from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
)
from business.device import Device
from business.sensor import Sensor

class DeviceForm(QDialog):
    def __init__(self, parent, callback_refresh, device=None):
        super().__init__(parent)

        self.callback_refresh = callback_refresh
        self.device_to_edit = device
        self.created_device = None
        self.edited = False

        self.setWindowTitle("Device Editor" if device else "Add Device")
        self.resize(300, 200)

        layout = QVBoxLayout()

        # --- NAME ---
        layout.addWidget(QLabel("Name:"))
        self.input_name = QLineEdit()
        layout.addWidget(self.input_name)

        # --- EXPECTED ---
        layout.addWidget(QLabel("Expected Consumption (W):"))
        self.input_expected = QLineEdit()
        layout.addWidget(self.input_expected)

        # --- BASE CURRENT ---
        layout.addWidget(QLabel("Base Current (A):"))
        self.input_current = QLineEdit()
        layout.addWidget(self.input_current)

        # PRELOAD IF EDITING
        if device:
            self.input_name.setText(device.name)
            self.input_expected.setText(str(device.expected_consumption))
            self.input_current.setText(str(device.sensor.base_current))

        # Buttons
        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self.save)

        layout.addWidget(btn_save)

        self.setLayout(layout)

    def save(self):
        name = self.input_name.text()
        expected = float(self.input_expected.text())
        base_current = float(self.input_current.text())

        # EDIT MODE
        if self.device_to_edit:
            self.device_to_edit.name = name
            self.device_to_edit.expected_consumption = expected
            self.device_to_edit.sensor.base_current = base_current

            self.callback_refresh()
            self.edited = True
            self.close()
            return

        # ADD MODE
        sensor = Sensor(base_voltage=120, base_current=base_current)
        self.created_device = Device(name, expected, sensor)
        self.callback_refresh()
        self.close()
