import time
import logging

logging.basicConfig(
    filename='taximeter.log',
    level=logging.INFO,
    format='%(asctime)s  %(levelname)s  %(funcName)s:%(lineno)d  %(message)s'
)
logger = logging.getLogger(__name__)

def calculate_fare(seconds_stopped, seconds_moving):
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05
    return fare

def taximeter():
    print("Bienvenidxs a TaxiMeter".center(len("La forma más justa de calcular el precio de tu viaje")))
    print("La forma mas justa de calcular el precio de tu viaje")
    print("[A] Comenzar viaje\n[B] Detener\n[C] Continuar\n[D] Finalizar\n[E] Nuevo viaje\n[F] Salir de TaxiMeter")

    trip_active = False
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None
    state_start_time = 0

# DIFERENCIAS CON EL EJEMPLO
# - Comandos: letras únicas (a,b,c,d,e,f) en vez de palabras completas
# - Idioma: mensajes al usuario en español
# - Comando 'a': arranca en 'moving' (€0.05/seg) porque el taxi sale directo
# - Comando 'e': ya no finaliza el viaje activo -- si hay viaje activo avisa, si no hay resetea contadores
# - start_time: ahora se usa para calcular y mostrar la duración total del viaje al finalizar con D
# - logger: usa __name__ como nombre (nombre del archivo) para identificar el origen del log si el proyecto crece
# - bugfix state_start_time: al cambiar de estado (b/c) se reinicia state_start_time para medir cada tramo desde su inicio, no desde el inicio del viaje

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
            elif opcion in ("b", "c"):
                if not trip_active:
                    print("No hay un viaje activo. Por favor ingrese el comando A para comenzar.")
                    continue
                duration = time.time() - state_start_time
                if state == 'stopped':
                    stopped_time += duration
                else:
                    moving_time += duration
                new_state = 'stopped' if opcion == "b" else 'moving'
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
                total_fare = calculate_fare(stopped_time, moving_time)
                print(f"\n Viaje finalizado")
                print(f"\n Duración total: {total_duration:.1f} segundos")
                print(f"\n Tiempo detenido: {stopped_time:.1f} segundos -- €{stopped_time * 0.02:.2f}")
                print(f"\n Tiempo en movimiento: {moving_time:.1f} segundos -- €{moving_time * 0.05:.2f}")
                print(f"\n\nTotal: €{total_fare:.2f}")
                logger.info("Viaje finalizado -- duración: %.1fs | detenido: %.1fs (€%.2f) | movimiento: %.1fs (€%.2f) | total: €%.2f",
                            total_duration, stopped_time, stopped_time * 0.02, moving_time, moving_time * 0.05, total_fare)  # resumen completo para control o disputas de tarifa
                trip_active = False
                state = None
            elif opcion == "e":
                if trip_active:
                    print("Viaje en curso. Pulse D para finalizarlo.")
                else:
                    stopped_time = 0
                    moving_time = 0
                    state = None
                    print("Pulse A para comenzar un nuevo viaje.")
                    logger.info("Contadores reiniciados")  # confirmar que el reset fue intencional y no un bug
            elif opcion == "f":
                print("Gracias por usar Taximeter. ¡Hasta Pronto!")
                logger.info("Programa cerrado por el usuario")  # distinguir cierre normal de un crash
                break
            else:
                logger.warning("Comando no reconocido: '%s'", opcion)  # detectar errores de tipeo o uso incorrecto
                print("Comando no reconocido. Use A, B, C, D, E o F.")
    except Exception:
        logger.exception("Error inesperado")  # capturar cualquier crash no previsto con stack trace completo

if __name__ == "__main__":
    taximeter()
