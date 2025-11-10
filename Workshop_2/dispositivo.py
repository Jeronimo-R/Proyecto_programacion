class Dispositivo:
    def __init__(self, nombre, tipo, estado=False):
        self.nombre = nombre
        self.tipo = tipo
        self.estado = estado

    def encender(self):
        self.estado = True

    def apagar(self):
        self.estado = False

    def __str__(self):
        estado_str = "Encendido" if self.estado else "Apagado"
        return f"Dispositivo: {self.nombre} ({self.tipo}) - Estado: {estado_str}"
