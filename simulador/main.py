from models.sensor import Sensor
from models.device import Device
from models.device_manager import DeviceManager
from gui.main_gui import start_gui


sensor1 = Sensor(base_voltage=120, base_current=0.7)
sensor2 = Sensor(base_voltage=120, base_current=0.3)
sensor3 = Sensor(base_voltage=120, base_current=0.9)
sensor4 = Sensor(base_voltage=120, base_current=0.15)

device1 = Device("Refrigerator", expected_consumption=150, sensor=sensor1)
device2 = Device("Television", expected_consumption=80, sensor=sensor2)
device3 = Device("Air Conditioner", expected_consumption=1200, sensor=sensor3)
device4 = Device("Laptop", expected_consumption=65, sensor=sensor4)

devices = [device1, device2, device3, device4]

manager = DeviceManager(devices)

if __name__ == "__main__":
    start_gui(manager)
