import time
import logging
from datetime import datetime

logging.basicConfig(
    filename='taximeter.log',
    level=logging.INFO,
    format='%(asctime)s  %(levelname)s  %(funcName)s:%(lineno)d  %(message)s'
)
logger = logging.getLogger(__name__)

def load_rates():
    with open("tarifas.txt", "r") as file:
        lines = file.readlines()
    return float(lines[0]), float(lines[1])

def calculate_fare(seconds_stopped, seconds_moving, rates_stopped=0.02, rate_moving=0.05):
    fare = seconds_stopped * rates_stopped + seconds_moving * rate_moving
    return fare

def taximeter():
    print("Bienvenidxs a TaxiMeter".center(len("La forma más justa de calcular el precio de tu viaje")))
    print("La forma mas justa de calcular el precio de tu viaje")
    print("[A] Comenzar viaje\n[B] Detener\n[C] Continuar\n[D] Finalizar\n[E] Nuevo viaje\n[T] Configurar tarifas\n[F] Salir de TaxiMeter")

    trip_active = False
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None
    state_start_time = 0
    rate_stopped, rate_moving = load_rates()

    # DIFERENCIAS CON EL EJEMPLO
    # - Comandos: letras únicas (a,b,c,d,e,f) en vez de palabras completas
    # - Idioma: mensajes al usuario en español
    # - Comando 'a': arranca en 'moving' (€0.05/seg) porque el taxi sale directo
    # - Comando 'e': ya no finaliza el viaje activo -- si hay viaje activo avisa, si no hay resetea contadores
    # - start_time: ahora se usa para calcular y mostrar la duración total del viaje al finalizar con D
    # - logger: usa __name__ como nombre (nombre del archivo) para identificar el origen del log si el proyecto crece

    try:
        while True:
            opcion = input("Elija un comando: ").strip().lower()
            if opcion == "a":
                if trip_active:
                    print("Viaje en progreso")
                    continue
                trip_active = True
                start_time = time.time()
                stopped_time = 0
                moving_time = 0
                state = 'moving'
                state_start_time = time.time()
                print("Inicio de viaje")
                logger.info("Viaje iniciado")  # trazabilidad: saber cuándo arrancó cada viaje
            elif opcion == "b":
                if not trip_active:
                    print("No hay un viaje activo. Por favor ingrese el comando A para comenzar.")
                    continue
                if state == "stopped":
                    print("El viaje esta detenido. Por favor ingrese el comando C para retomarlo o D para finalizar.")
                    continue
                duration = time.time() - state_start_time
                moving_time += duration
                new_state = 'stopped'
                logger.info("Estado cambiado: %s -> %s (duración tramo: %.1fs)", state, new_state, duration)  # detectar patrones de uso: paradas frecuentes o largas
                state = new_state
                state_start_time = time.time()
            elif opcion == "c":
                if not trip_active:
                    print("No hay un viaje activo. Por favor ingrese el comando A para comenzar.")
                    continue
                if state == "moving": 
                    print("Viaje en progreso. Para detenerlo ingrese B. Si desea finalizarlo ingrese D")
                    continue
                duration = time.time() - state_start_time
                stopped_time += duration
                new_state = 'moving' 
                logger.info("Estado cambiado: %s -> %s (duración tramo: %.1fs)", state, new_state, duration)  # detectar patrones de uso: paradas frecuentes o largas
                state = new_state
                state_start_time = time.time()
            elif opcion == "d":
                if not trip_active:
                    print("No hay un viaje activo. Por favor ingrese el comando A para comenzar.")
                    continue
                duration = time.time() - state_start_time
                if state == 'stopped':
                    stopped_time += duration
                else:
                    moving_time += duration
                total_duration = time.time() - start_time
                total_fare = calculate_fare(stopped_time, moving_time, rate_stopped, rate_moving)
                print(f"\n Viaje finalizado")
                print(f"\n Duración total: {total_duration:.1f} segundos")
                print(f"\n Tiempo detenido: {stopped_time:.1f} segundos -- €{stopped_time * rate_stopped:.2f}")
                print(f"\n Tiempo en movimiento: {moving_time:.1f} segundos -- €{moving_time * rate_moving:.2f}")
                print(f"\n\nTotal: €{total_fare:.2f}")
                logger.info("Viaje finalizado -- duración: %.1fs | detenido: %.1fs (€%.2f) | movimiento: %.1fs (€%.2f) | total: €%.2f",
                            total_duration, stopped_time, stopped_time * 0.02, moving_time, moving_time * 0.05, total_fare)  # resumen completo para control o disputas de tarifa
                trip_active = False
                state = None
                with open("historial.txt", "a") as file:
                    file.write(
                        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | "
                        f"Duración: {total_duration:.1f}s | "
                        f"Parado: {stopped_time:.1f}s (€{stopped_time * 0.02:.2f}) | "
                        f"Movimiento: {moving_time:.1f}s (€{moving_time * 0.05:.2f}) | "
                        f"Total: €{total_fare:.2f}\n"
                    )
            elif opcion == "e":
                if trip_active:
                    print("Viaje en curso. Pulse D para finalizarlo.")
                else:
                    stopped_time = 0
                    moving_time = 0
                    state = None
                    print("Pulse A para comenzar un nuevo viaje.")
                    logger.info("Contadores reiniciados")  # confirmar que el reset fue intencional y no un bug
            elif opcion == "t":
                if trip_active:
                    print("Hay un viaje en curso. Finalizalo antes de cambiar las tarifas.")
                    continue
                new_rate_stopped = input(f"Tarifa por segundo detenido (actual: €{rate_stopped}): ").strip()
                new_rate_moving = input(f"Tarifa por segundo en movimiento (actual: €{rate_moving}): ").strip()
                confirmacion = input("Ingrese 1 para confirmar o cualquier tecla para cancelar: ").strip()
                if confirmacion == "1":
                    rate_stopped = float(new_rate_stopped)
                    rate_moving = float(new_rate_moving)
                    with open("tarifas.txt", "w") as file:
                        file.write(f"{rate_stopped}\n{rate_moving}\n")
                    print("Tarifas actualizadas correctamente.")
                    logger.info("Tarifas actualizadas -- parado: €%.2f | movimiento: €%.2f", rate_stopped, rate_moving)
            elif opcion == "f":
                if trip_active:
                    print("Hay un viaje en curso. Finalizalo antes de apagar el Taximeter.")
                    continue
                print("Gracias por usar Taximeter. ¡Hasta Pronto!")
                logger.info("Programa cerrado por el usuario")  # distinguir cierre normal de un crash
                break
            else:
                logger.warning("Comando no reconocido: '%s'", opcion)  # detectar errores de tipeo o uso incorrecto
                print("Comando no reconocido. Use A, B, C, D, E, T o F.")
    except Exception:
        logger.exception("Error inesperado")  # capturar cualquier crash no previsto con stack trace completo

if __name__ == "__main__":
    taximeter()
