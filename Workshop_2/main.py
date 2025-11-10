from dispositivo import Dispositivo
from medidor_tiempo import MedidorTiempo
from medidor_watts import MedidorWatts
from medidor_costos import MedidorCostos

# Colocar nombre y tipo del dispositivo conectado
d1 = Dispositivo("Nevera", "Electrodoméstico")

# Poner nombre de los medidores (mas comodo asi)
horas = MedidorTiempo(d1.nombre)
potencia = MedidorWatts(d1.nombre)
costo = MedidorCostos(d1.nombre)

# Registrar datos de consumo
horas.agregar_tiempo(5) # 5 = 5 horas
potencia.agregar_potencia(1500)  # 1500 = 1500 Watts (W)
costo.registrar_consumo(1500, 5)
costo.registrar_consumo(1500, 56) # Potencia multiplicado por horas de consumo = Costo

# Imprimir resutlados
print(horas, horas.obtener_tiempos())
print(potencia, potencia.obtener_potencias())
costo.imprimir_costo_total() # Si se usa print, devuelve None
