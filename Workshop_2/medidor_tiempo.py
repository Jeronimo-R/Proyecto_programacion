from medidor import Medidor

class MedidorTiempo(Medidor):
    def __init__(self, dispositivo, tipo="Tiempo"):
        super().__init__(dispositivo, tipo)
        self.tiempos = []

    def agregar_tiempo(self, horas):
        self.tiempos.append(f"{horas} horas")

    def obtener_tiempos(self):
        return self.tiempos

