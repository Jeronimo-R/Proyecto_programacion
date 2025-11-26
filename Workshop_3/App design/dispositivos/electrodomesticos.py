from .dispositivo_base import DispositivoBase

class Nevera(DispositivoBase):
    def __init__(self, nombre: str, potencia: float, temperatura: float):
        super().__init__(nombre, potencia)
        self._temperatura = temperatura
    
    def calcular_consumo_energia(self, horas: float) -> float:
        consumo_base = super().calcular_consumo_energia(horas)
        return consumo_base * 1.3

class Television(DispositivoBase):
    def __init__(self, nombre: str, potencia: float, tamano_pantalla: int):
        super().__init__(nombre, potencia)
        self._tamano_pantalla = tamano_pantalla

class AireAcondicionado(DispositivoBase):
    def __init__(self, nombre: str, potencia: float, capacidad_btu: int):
        super().__init__(nombre, potencia)
        self._capacidad_btu = capacidad_btu
    
    def calcular_consumo_energia(self, horas: float) -> float:
        consumo_base = super().calcular_consumo_energia(horas)
        return consumo_base * 0.8