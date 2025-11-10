from medidor import Medidor

Costo_Kwh_COP = 789.46  # Costo Kwh en Colombia

class MedidorCostos(Medidor):
    def __init__(self, dispositivo, tipo="Costos"):
        super().__init__(dispositivo, tipo)
        self.registros = []   # Registra watts y horas

    def registrar_consumo(self, watts, horas):
        # Registra potencia y tiempo
        registro = {
            "potencia_w": watts,
            "horas": horas
        }
        self.registros.append(registro)

    def costo_total(self):
        # Calcula el costo total acumulado en COP
        total_kwh = 0
        for reg in self.registros:
            energia = (reg["potencia_w"] * reg["horas"]) / 1000
            total_kwh += energia
        
        return total_kwh * Costo_Kwh_COP

    def imprimir_costo_total(self):
        total = self.costo_total()
        print(f"Costo total de consumo para {self.dispositivo}: {total} COP")