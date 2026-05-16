from taximeter import Taximeter
import tkinter as tk

ventana = tk.Tk()
ventana.title("Taximeter")

taxi = Taximeter()

label_precio = tk.Label(ventana, text="€ 0.00", font=("Arial", 32))
label_precio.pack(pady=10)

label_estado = tk.Label(ventana, text="Estado: inactivo", font=("Arial", 12))
label_estado.pack(pady=5)

def actualizar_precio():
    precio = taxi.get_current_fare()
    label_precio.config(text=f"€ {precio:.2f}")
    ventana.after(1000, actualizar_precio)

def iniciar():
    taxi.start_trip()
    label_estado.config(text="El viaje ha comenzado")

def detener():
    taxi.stop_trip()
    label_estado.config(text="El Viaje se ha detenido")

def continuar():
    taxi.continue_trip()
    label_estado.config(text="El viaje ha sido retomado ")

def finalizar():
    taxi.end_trip()
    label_estado.config(text="Viaje finalizado")

def reset():
    taxi.reset()
    label_estado.config(text="Nuevo viaje")

def nueva_tarifa():
    taxi.update_rates()
    label_estado.config(text="Actualizar tarifas")

def cerrar():
    if taxi.trip_active:
        label_estado.config(text="Finalizá el viaje antes de salir.")
    else:
        ventana.destroy()

boton_iniciar = tk.Button(ventana, text="Comenzar viaje", command=iniciar, padx=10, pady=5, width=20)
boton_iniciar.pack(pady=5)

boton_detener = tk.Button(ventana, text="Detener viaje", command=detener, padx=10, pady=5, width=20)
boton_detener.pack(pady=5)

boton_continuar = tk.Button(ventana, text="Continuar viaje", command=continuar, padx=10, pady=5, width=20)
boton_continuar.pack(pady=5)

boton_finalizar = tk.Button(ventana, text="Finalizar viaje",command=finalizar, padx=10, pady=5, width=20)
boton_finalizar.pack(pady=5)

boton_nuevo = tk.Button(ventana, text="Nuevo viaje", command=reset, padx=10, pady=5, width=20)
boton_nuevo.pack(pady=5)

boton_tarifas = tk.Button(ventana, text="Configurar tarifas", command=nueva_tarifa, padx=10, pady=5, width=20)
boton_tarifas.pack(pady=5)

boton_salir = tk.Button(ventana, text="Salir de TaxiMeter", command=cerrar, padx=10, pady=5, width=20)
boton_salir.pack(pady=5)

actualizar_precio()
ventana.protocol("WM_DELETE_WINDOW", cerrar)
ventana.mainloop()
