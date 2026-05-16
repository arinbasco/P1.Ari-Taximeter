import time
import logging
from datetime import datetime
import sqlite3
import bcrypt

logging.basicConfig(
    filename='taximeter.log',
    level=logging.INFO,
    format='%(asctime)s  %(levelname)s  %(funcName)s:%(lineno)d  %(message)s'
)
logger = logging.getLogger(__name__)

def init_db():
    conn = sqlite3.connect("taximeter.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            fecha TEXT,
            duracion REAL,
            tiempo_detenido REAL,
            tiempo_movimiento REAL,
            precio REAL
        )
    """)
    conn.commit()
    conn.close()


def create_user ():
    conn = sqlite3.connect("taximeter.db")
    cursor = conn.cursor()
    username = input("Usuario: ")
    password = input("Contraseña: ")
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        conn.close()
        print("Usuario creado correctamente.")
        return True
    except Exception as e:
        print("El usuario ya esta registrado. Intente nuevamente")
        conn.close()
        return False



def authenticate():
    conn = sqlite3.connect("taximeter.db")
    cursor = conn.cursor()
    print("=== Taximeter ===\nInicio de sesión")
    username = input("Usuario: ")
    password = input("Contraseña: ")
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        if bcrypt.checkpw(password.encode(), user[2]):
            conn.close()
            return user[0]
        else: 
            conn.close()
            print("Contraseña incorrecta.")
            return None
    else:
        print("Usuario no encontrado")
        conn.close()
        return None


class Taximeter:

    def __init__(self):
        self.trip_active = False
        self.start_time = 0
        self.stopped_time = 0
        self.moving_time = 0
        self.state = None
        self.state_start_time = 0
        self.rate_stopped, self.rate_moving = self.load_rates()
        self.user_id = None

    def load_rates(self):
        with open("tarifas.txt", "r") as file:
            lines = file.readlines()
        return float(lines[0]), float(lines[1])

    def calculate_fare(self):
        return self.stopped_time * self.rate_stopped + self.moving_time * self.rate_moving

    def get_current_fare(self):
        if not self.trip_active:
            return self.calculate_fare()
        elapsed = time.time() - self.state_start_time
        if self.state == 'moving':
            return (self.moving_time + elapsed) * self.rate_moving + self.stopped_time * self.rate_stopped
        else:
            return self.moving_time * self.rate_moving + (self.stopped_time + elapsed) * self.rate_stopped

    def start_trip(self):
        if self.trip_active:
            print("Viaje en progreso")
            return
        self.trip_active = True
        self.start_time = time.time()
        self.stopped_time = 0
        self.moving_time = 0
        self.state = 'moving'
        self.state_start_time = time.time()
        print("Inicio de viaje")
        logger.info("Viaje iniciado")

    def stop_trip(self):
        if not self.trip_active:
            print("No hay un viaje activo. Por favor ingrese el comando A para comenzar.")
            return
        if self.state == "stopped":
            print("El viaje esta detenido. Por favor ingrese el comando C para retomarlo o D para finalizar.")
            return
        duration = time.time() - self.state_start_time
        self.moving_time += duration
        new_state = 'stopped'
        logger.info("Estado cambiado: %s -> %s (duración tramo: %.1fs)", self.state, new_state, duration)
        self.state = new_state
        self.state_start_time = time.time()

    def continue_trip(self):
        if not self.trip_active:
            print("No hay un viaje activo. Por favor ingrese el comando A para comenzar.")
            return
        if self.state == "moving":
            print("Viaje en progreso. Para detenerlo ingrese B. Si desea finalizarlo ingrese D")
            return
        duration = time.time() - self.state_start_time
        self.stopped_time += duration
        new_state = 'moving'
        logger.info("Estado cambiado: %s -> %s (duración tramo: %.1fs)", self.state, new_state, duration)
        self.state = new_state
        self.state_start_time = time.time()

    def end_trip(self):
        if not self.trip_active:
            print("No hay un viaje activo. Por favor ingrese el comando A para comenzar.")
            return
        duration = time.time() - self.state_start_time
        if self.state == 'stopped':
            self.stopped_time += duration
        else:
            self.moving_time += duration
        total_duration = time.time() - self.start_time
        total_fare = self.calculate_fare()
        print(f"\n Viaje finalizado")
        print(f"\n Duración total: {total_duration:.1f} segundos")
        print(f"\n Tiempo detenido: {self.stopped_time:.1f} segundos -- €{self.stopped_time * self.rate_stopped:.2f}")
        print(f"\n Tiempo en movimiento: {self.moving_time:.1f} segundos -- €{self.moving_time * self.rate_moving:.2f}")
        print(f"\n\nTotal: €{total_fare:.2f}")
        logger.info("Viaje finalizado -- duración: %.1fs | detenido: %.1fs (€%.2f) | movimiento: %.1fs (€%.2f) | total: €%.2f",
                    total_duration, self.stopped_time, self.stopped_time * self.rate_stopped,
                    self.moving_time, self.moving_time * self.rate_moving, total_fare)
        self.trip_active = False
        self.state = None
        conn = sqlite3.connect("taximeter.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trips (user_id, fecha, duracion, tiempo_detenido, tiempo_movimiento, precio)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.user_id,
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            round(total_duration, 1),
            round(self.stopped_time, 1),
            round(self.moving_time, 1),
            round(total_fare, 2)
        ))
        conn.commit()
        conn.close()

    def reset(self):
        if self.trip_active:
            print("Viaje en curso. Pulse D para finalizarlo.")
            return
        self.stopped_time = 0
        self.moving_time = 0
        self.state = None
        print("Pulse A para comenzar un nuevo viaje.")
        logger.info("Contadores reiniciados")

    def update_rates(self):
        if self.trip_active:
            print("Hay un viaje en curso. Finalizalo antes de cambiar las tarifas.")
            return
        new_rate_stopped = input(f"Tarifa por segundo detenido (actual: €{self.rate_stopped}): ").strip()
        new_rate_moving = input(f"Tarifa por segundo en movimiento (actual: €{self.rate_moving}): ").strip()
        confirmacion = input("Ingrese 1 para confirmar o cualquier tecla para cancelar: ").strip()
        if confirmacion == "1":
            self.rate_stopped = float(new_rate_stopped)
            self.rate_moving = float(new_rate_moving)
            with open("tarifas.txt", "w") as file:
                file.write(f"{self.rate_stopped}\n{self.rate_moving}\n")
            print("Tarifas actualizadas correctamente.")
            logger.info("Tarifas actualizadas -- parado: €%.2f | movimiento: €%.2f", self.rate_stopped, self.rate_moving)

    def run(self):
        print("Bienvenidxs a TaxiMeter".center(len("La forma más justa de calcular el precio de tu viaje")))
        print("La forma mas justa de calcular el precio de tu viaje")
        print("[A] Comenzar viaje\n[B] Detener\n[C] Continuar\n[D] Finalizar\n[E] Nuevo viaje\n[T] Configurar tarifas\n[F] Salir de TaxiMeter")
        try:
            while True:
                opcion = input("Elija un comando: ").strip().lower()
                if opcion == "a":
                    self.start_trip()
                elif opcion == "b":
                    self.stop_trip()
                elif opcion == "c":
                    self.continue_trip()
                elif opcion == "d":
                    self.end_trip()
                elif opcion == "e":
                    self.reset()
                elif opcion == "t":
                    self.update_rates()
                elif opcion == "f":
                    if self.trip_active:
                        print("Hay un viaje en curso. Finalizalo antes de apagar el taxímetro.")
                        continue
                    print("Gracias por usar Taximeter. ¡Hasta Pronto!")
                    logger.info("Programa cerrado por el usuario")
                    break
                else:
                    logger.warning("Comando no reconocido: '%s'", opcion)
                    print("Comando no reconocido. Use A, B, C, D, E, T o F.")
        except Exception:
            logger.exception("Error inesperado")


if __name__ == "__main__":
    init_db()
    opcion = input("[1] Iniciar sesión\n[2] Registrar usuario\n[F] Salir\nElegí un comando: ").strip().lower()
    if opcion == "1":
        intentos = 0
        while intentos < 3:
            user_id = authenticate()
            if user_id:
                taxi = Taximeter()
                taxi.user_id = user_id
                taxi.run()
                break
            else:
                intentos += 1
        else:
            print("Superaste la cantidad de intentos fallidos. Vuelve a iniciar Taximeter.")
    elif opcion == "2":
        while True:
            if create_user():
                break
        intentos = 0
        while intentos < 3:
            user_id = authenticate()
            if user_id:
                taxi = Taximeter()
                taxi.user_id = user_id
                taxi.run()
                break
            else:
                intentos += 1
        else:
            print("Superaste la cantidad de intentos fallidos. Vuelve a iniciar Taximeter.")
    elif opcion == "f":
        print("Gracias por usar Taximeter. ¡Hasta Pronto!")
        exit()