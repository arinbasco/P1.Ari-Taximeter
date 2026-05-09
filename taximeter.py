import time

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
        elif opcion in ("b", "c"):
            if not trip_active:
                print("No hay un viaje activo. Por favor ingrese el comando A para comenzar.")
                continue
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration
            state = 'stopped' if opcion == "b" else 'moving' 
        elif opcion == "d":
            if not trip_active:
                print("No hay un viaje activo. Por favor ingrese el comando A para comenzar.")
                continue
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration
            total_fare = calculate_fare(stopped_time, moving_time)
            print(f"\n Viaje finalizado")
            print(f"\n Tiempo detenido: {stopped_time:.1f} segundos -- €{stopped_time * 0.02:.2f}")
            print(f"\n Tiempo en movimiento: {moving_time:.1f} segundos -- €{moving_time * 0.05:.2f}")
            print(f"\n\nTotal: €{total_fare:.2f}")
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
        elif opcion == "f":
            print("Gracias por usar Taximeter. ¡Hasta Pronto!")
            break
        else:
            print("Comando no reconocido. Use A, B, C, D, E o F.")

taximeter()
