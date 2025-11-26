from abc import ABC, abstractmethod

class ICanalNotificacion(ABC):
    @abstractmethod
    def enviar_alerta(self, mensaje: str) -> bool:
        pass

class NotificadorConsola(ICanalNotificacion):
    def enviar_alerta(self, mensaje: str) -> bool:
        print(f"🚨 ALERTA: {mensaje}")
        return True