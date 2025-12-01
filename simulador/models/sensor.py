import random
from datetime import datetime
from models.measurement import Measurement


class Sensor:
    def __init__(self, base_voltage=120, base_current=0.5):
        self.base_voltage = base_voltage
        self.base_current = base_current
        self.accumulated_energy = 0  # Wh

    def generate_measurement(self):
        voltage = self.base_voltage + random.uniform(-2, 2)
        current = self.base_current + random.uniform(-0.1, 0.1)

        power = voltage * current  # Watts
        energy_wh = power * (1 / 60)  # 1 second ≡ 1 minute virtual = 1/60 h

        self.accumulated_energy += energy_wh

        return Measurement(
            timestamp=datetime.now(),
            voltage=round(voltage, 2),
            current=round(current, 3),
            power=round(power, 2),
            energy=round(self.accumulated_energy, 4)
        )
