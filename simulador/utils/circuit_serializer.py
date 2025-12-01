import json
from business.device_manager import DeviceManager
from business.device import Device
from business.sensor import Sensor


def save_circuit(filename, manager):
    data = []

    for d in manager.get_all():
        data.append({
            "name": d.name,
            "expected_consumption": d.expected_consumption,
            "sensor": {
                "base_voltage": d.sensor.base_voltage,
                "base_current": d.sensor.base_current,
                "accumulated_energy": d.sensor.accumulated_energy
            },
            "monthly_history": d.monthly_history
        })

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_circuit(filename):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except:
        return None

    devices = []

    for item in data:
        sdata = item["sensor"]
        sensor = Sensor(sdata["base_voltage"], sdata["base_current"])
        sensor.accumulated_energy = sdata["accumulated_energy"]

        device = Device(item["name"], item["expected_consumption"], sensor)
        device.monthly_history = item.get("monthly_history", [])

        devices.append(device)

    return DeviceManager(devices)
