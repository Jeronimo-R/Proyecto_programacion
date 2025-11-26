from typing import List, Dict, Tuple
from dispositivos.dispositivo_base import DispositivoBase

class CalculadorEnergia:
    def __init__(self, tarifa_cop: float = 450.0):
        self._tarifa_cop = tarifa_cop
    
    def calcular_costo_total(self, dispositivos: List[DispositivoBase], 
                           horas_uso: Dict[str, float]) -> Dict:
        total_costo = 0.0
        detalles = {}
        
        for dispositivo in dispositivos:
            if dispositivo.nombre in horas_uso:
                consumo_kwh = dispositivo.calcular_consumo_energia(horas_uso[dispositivo.nombre])
                costo = consumo_kwh * self._tarifa_cop
                detalles[dispositivo.nombre] = {
                    'consumo_kwh': consumo_kwh,
                    'costo_cop': costo
                }
                total_costo += costo
        
        return {
            'detalles': detalles,
            'total': total_costo
        }
    
    def generar_ranking(self, dispositivos: List[DispositivoBase], 
                       horas_uso: Dict[str, float]) -> List[Tuple[str, float]]:
        consumo_dispositivos = []
        
        for dispositivo in dispositivos:
            if dispositivo.nombre in horas_uso:
                consumo = dispositivo.calcular_consumo_energia(horas_uso[dispositivo.nombre])
                consumo_dispositivos.append((dispositivo.nombre, consumo))
        
        return sorted(consumo_dispositivos, key=lambda x: x[1], reverse=True)