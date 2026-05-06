def taximeter ():
  print("Bienvenidxs a TaxiMeter".center(len("La forma más justa de calcular el precio de tu viaje")))
  print("La forma mas justa de calcular el precio de tu viaje")
  print ("[A] Comenzar viaje\n[B] Detener\n[C] Continuar\n[D] Finalizar\n[E] Nuevo viaje\n[F] Salir de TaxiMeter")
  while True:
    opcion = input("Elija un comando: ")

    if opcion == "F":
      print("Gracias por usar Taximeter. ¡Hasta Pronto!")
      break
taximeter()
