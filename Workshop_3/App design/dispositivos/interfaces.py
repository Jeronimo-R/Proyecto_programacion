from abc import ABC, abstractmethod
from typing import Dict

class IConsumibleEnergia(ABC):
    @abstractmethod
    def calcular_consumo_energia(self, horas: float) -> float:
        pass

class INotificable(ABC):
    @abstractmethod
    def obtener_info_notificacion(self) -> Dict:
        pass

class IPersistible(ABC):
    @abstractmethod
    def a_diccionario(self) -> Dict:
        pass