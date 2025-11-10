from medidor import Medidor

class MedidorWatts(Medidor):
    def __init__(self, dispositivo, tipo="Potencia"):
        super().__init__(dispositivo, tipo)
        self.potencia = []

    def agregar_potencia(self, watts):
        self.potencia.append(f"{watts} watts")

    def obtener_potencias(self):
        return self.potencia
