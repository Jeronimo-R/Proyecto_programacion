from abc import ABC, abstractmethod
from typing import Dict

class ISensor(ABC):
    @abstractmethod
    def obtener_lectura(self) -> Dict[str, float]:
        pass

class SensorBase(ISensor):
    def __init__(self, nombre: str):
        self._nombre = nombre
    
    @property
    def nombre(self) -> str:
        return self._nombre