from .interfaces import IConsumibleEnergia, INotificable, IPersistible
from typing import Dict

class DispositivoBase(IConsumibleEnergia, INotificable, IPersistible):
    def __init__(self, nombre: str, potencia: float):
        self._nombre = nombre
        self._potencia = potencia
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        self._nombre = nuevo_nombre
    
    @property
    def potencia(self) -> float:
        return self._potencia
    
    def calcular_consumo_energia(self, horas: float) -> float:
        return (self._potencia * horas) / 1000
    
    def obtener_info_notificacion(self) -> Dict:
        return {
            "nombre": self._nombre,
            "potencia": self._potencia,
            "tipo": self.__class__.__name__
        }
    
    def a_diccionario(self) -> Dict:
        return {
            "nombre": self._nombre,
            "potencia": self._potencia,
            "tipo": self.__class__.__name__
        }
    
    def __str__(self) -> str:
        return f"{self._nombre} - {self._potencia}W"