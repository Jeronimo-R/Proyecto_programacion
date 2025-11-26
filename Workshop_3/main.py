from dispositivos import Nevera, Television, AireAcondicionado
from servicios import GestorDispositivos, CalculadorEnergia, NotificadorConsola
from sensores import SensorSimulado
from utils import TARIFA_COP

def main():
    print("🚀 Simulador de Consumo Energético - FUNCIONANDO")
    
    # Crear servicios
    gestor = GestorDispositivos()
    calculador = CalculadorEnergia(TARIFA_COP)
    notificador = NotificadorConsola()
    
    # Agregar dispositivos
    dispositivos = [
        Nevera("Nevera Cocina", 150, 4),
        Television("TV Sala", 100, 55),
        AireAcondicionado("AC Dormitorio", 1200, 12000)
    ]
    
    for dispositivo in dispositivos:
        gestor.registrar_dispositivo(dispositivo)
        print(f"✅ Agregado: {dispositivo}")
    
    # Calcular consumo
    horas_uso = {
        "Nevera Cocina": 24, 
        "TV Sala": 6, 
        "AC Dormitorio": 8
    }
    
    resultado = calculador.calcular_costo_total(
        gestor.obtener_todos(), 
        horas_uso
    )
    
    print(f"\n💰 COSTOS DIARIOS:")
    for nombre, datos in resultado['detalles'].items():
        print(f"   {nombre}: ${datos['costo_cop']:,.0f} COP")
    print(f"   TOTAL: ${resultado['total']:,.0f} COP")
    
    # Mostrar ranking
    ranking = calculador.generar_ranking(gestor.obtener_todos(), horas_uso)
    print(f"\n🏆 RANKING DE CONSUMO:")
    for i, (nombre, consumo) in enumerate(ranking, 1):
        print(f"   {i}. {nombre}: {consumo:.2f} kWh")
    
    # Probar sensor
    sensor = SensorSimulado()
    lectura = sensor.obtener_lectura()
    print(f"\n📊 Lectura del sensor:")
    print(f"   Potencia: {lectura['potencia']:.1f}W")
    print(f"   Voltaje: {lectura['voltaje']:.1f}V")
    
    # Probar notificación
    notificador.enviar_alerta("Sistema inicializado correctamente")

if __name__ == "__main__":
    main()