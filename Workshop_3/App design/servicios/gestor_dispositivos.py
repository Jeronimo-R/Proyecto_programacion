from typing import List, Optional
from dispositivos.dispositivo_base import DispositivoBase

class GestorDispositivos:
    def __init__(self):
        self._dispositivos: List[DispositivoBase] = []
    
    def registrar_dispositivo(self, dispositivo: DispositivoBase):
        self._dispositivos.append(dispositivo)
    
    def obtener_por_nombre(self, nombre: str) -> Optional[DispositivoBase]:
        for dispositivo in self._dispositivos:
            if dispositivo.nombre == nombre:
                return dispositivo
        return None
    
    def obtener_todos(self) -> List[DispositivoBase]:
        return self._dispositivos.copy()
    
    def contar_dispositivos(self) -> int:
        return len(self._dispositivos)