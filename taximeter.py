import time

def calculate_fare(seconds_stopped, seconds_moving):
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05
    print(f"Total: {fare}")
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
            state = 'stopped'
            state_start_time = time.time()
            print("Inicio de viaje")
        elif opcion in ("b", "c", "e", "f"):
            if not trip_active:
                print("No hay un viaje activo. Por favor ingrese el comando A para comenzar.")
                continue
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration
        if opcion == "f":
            print("Gracias por usar Taximeter. ¡Hasta Pronto!")
            break

taximeter()
