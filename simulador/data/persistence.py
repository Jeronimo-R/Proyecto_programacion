import json
from business.device import Device
from business.sensor import Sensor
from business.device_manager import DeviceManager
from business.measurement import Measurement
from datetime import datetime


def save_to_file(device_manager, filename="circuit.json"):
    data = {"devices": []}

    for d in device_manager.get_all():
        device_data = {
            "name": d.name,
            "expected_consumption": d.expected_consumption,
            "sensor": {
                "base_voltage": d.sensor.base_voltage,
                "base_current": d.sensor.base_current,
                "accumulated_energy": d.sensor.accumulated_energy
            },
            "history": [
                {
                    "timestamp": m.timestamp.isoformat(),
                    "voltage": m.voltage,
                    "current": m.current,
                    "power": m.power,
                    "energy": m.energy
                }
                for m in d.history
            ],
            "monthly_history": d.monthly_history,
            "alerts": d.alerts
        }

        data["devices"].append(device_data)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def load_from_file(filename="circuit.json"):
    with open(filename, "r") as f:
        data = json.load(f)

    devices = []

    for d in data["devices"]:
        sensor = Sensor(
            base_voltage=d["sensor"]["base_voltage"],
            base_current=d["sensor"]["base_current"]
        )
        sensor.accumulated_energy = d["sensor"]["accumulated_energy"]

        dev = Device(
            d["name"],
            d["expected_consumption"],
            sensor
        )

        # Restore history
        for m in d["history"]:
            dev.history.append(
                Measurement(
                    timestamp=datetime.fromisoformat(m["timestamp"]),
                    voltage=m["voltage"],
                    current=m["current"],
                    power=m["power"],
                    energy=m["energy"],
                )
            )

        dev.monthly_history = d["monthly_history"]
        dev.alerts = d.get("alerts", [])

        devices.append(dev)

    return DeviceManager(devices)
