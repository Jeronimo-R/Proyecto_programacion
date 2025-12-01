import sys
from PyQt5.QtWidgets import QApplication

from business.device_manager import DeviceManager
from business.device import Device
from business.sensor import Sensor
from presentation.main_window import MainWindow


def main():
    # Sample devices
    sensor1 = Sensor(120, 0.7)
    sensor2 = Sensor(120, 0.3)
    sensor3 = Sensor(120, 0.9)
    sensor4 = Sensor(120, 0.15)

    device1 = Device("Refrigerator", 150, sensor1)
    device2 = Device("Television", 80, sensor2)
    device3 = Device("Air Conditioner", 1200, sensor3)
    device4 = Device("Laptop", 65, sensor4)

    devices = [device1, device2, device3, device4]

    manager = DeviceManager(devices)

    app = QApplication(sys.argv)
    win = MainWindow(manager)
    win.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
