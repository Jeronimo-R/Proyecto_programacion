class Medidor:
    def __init__(self, dispositivo, tipo):
        self.dispositivo = dispositivo
        self.tipo = tipo

    def __str__(self):
        return f"Medidor {self.dispositivo} ({self.tipo})"
