from sensor_base import SensorBase
from typing import Dict
import random
from datetime import datetime

class SensorSimulado(SensorBase):
    def __init__(self):
        super().__init__("Sensor Simulado")
    
    def obtener_lectura(self) -> Dict[str, float]:
        return {
            "voltaje": 220.0 + random.uniform(-5, 5),
            "corriente": random.uniform(1, 10),
            "potencia": random.uniform(100, 1500),
            "timestamp": datetime.now().isoformat()
        }