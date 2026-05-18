from flask import Flask, render_template, session, redirect, url_for, request, flash
from taximeter import Taximeter
import sqlite3
import bcrypt
import logging
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "taximeter_secret_key"

taxi = Taximeter()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    precio_actual = round(taxi.get_current_fare(), 2)
    return render_template('index.html', precio=precio_actual)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("taximeter.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(password.encode(), user[2]):
            session['user_id'] = user[0]
            taxi.user_id = user[0]
            return redirect(url_for('index'))
        return render_template('login.html', error="Usuario o contraseña incorrectos")
    return render_template('login.html')

@app.route('/iniciar', methods=['POST'])
def iniciar():
    if taxi.trip_active:
        flash("Viaje en progreso.")
    else:
        taxi.start_trip()
        flash("Viaje iniciado.")
    return redirect(url_for('index'))

@app.route('/detener', methods=['POST'])
def detener():
    if not taxi.trip_active:
        flash("No hay un viaje activo.")
    elif taxi.state == 'stopped':
        flash("El viaje ya está detenido. Retomalo con Continuar o finalizalo.")
    else:
        taxi.stop_trip()
        flash("Viaje detenido.")
    return redirect(url_for('index'))

@app.route('/continuar', methods=['POST'])
def continuar():
    if not taxi.trip_active:
        flash("No hay un viaje activo.")
    elif taxi.state == 'moving':
        flash("Viaje en progreso. Para detenerlo usá Detener.")
    else:
        taxi.continue_trip()
        flash("Viaje retomado.")
    return redirect(url_for('index'))

@app.route('/finalizar', methods=['POST'])
def finalizar():
    if not taxi.trip_active:
        flash("No hay un viaje activo.")
        return redirect(url_for('index'))
    taxi.end_trip()
    return redirect(url_for('resumen'))

@app.route('/resumen')
def resumen():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect("taximeter.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, duracion, tiempo_detenido, tiempo_movimiento, precio FROM trips WHERE user_id = ? ORDER BY id DESC LIMIT 1", (session['user_id'],))
    viaje = cursor.fetchone()
    conn.close()
    return render_template('resumen.html', viaje=viaje)

@app.route('/reset', methods=['POST'])
def reset():
    if taxi.trip_active:
        flash("Hay un viaje en curso. Finalizalo antes de reiniciar.")
    else:
        taxi.reset()
        flash("Listo para un nuevo viaje.")
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    if taxi.trip_active:
        flash("Finalizá el viaje antes de cerrar sesión.")
        return redirect(url_for('index'))
    session.clear()
    return redirect(url_for('login'))

@app.route('/precio')
def precio():
    return str(round(taxi.get_current_fare(), 2))

@app.route('/tarifas', methods=['GET', 'POST'])
def tarifas():
    if taxi.trip_active:
        flash("Hay un viaje en curso. Finalizalo antes de cambiar las tarifas.")
        return redirect(url_for('index'))
    if request.method == 'POST':
        nueva_parado = request.form['rate_stopped']
        nueva_movimiento = request.form['rate_moving']
        confirmacion = request.form.get('confirmacion')
        if confirmacion == '1':
            taxi.rate_stopped = float(nueva_parado)
            taxi.rate_moving = float(nueva_movimiento)
            with open("tarifas.txt", "w") as file:
                file.write(f"{taxi.rate_stopped}\n{taxi.rate_moving}\n")
            logger.info("Tarifas actualizadas -- parado: €%.2f | movimiento: €%.2f", taxi.rate_stopped, taxi.rate_moving)
            flash("Tarifas actualizadas correctamente.")
            return redirect(url_for('index'))
        else:
            flash("Las tarifas no han sido modificadas.")
            return redirect(url_for('index'))
    return render_template('tarifas.html',
            rate_stopped=taxi.rate_stopped,
            rate_moving=taxi.rate_moving)

@app.route('/historial')
def historial():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if taxi.trip_active:
        flash("Hay un viaje en curso. Finalizalo para ver el historial.")
        return redirect(url_for('index'))
    conn = sqlite3.connect("taximeter.db")
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, duracion, tiempo_detenido, tiempo_movimiento, precio FROM trips WHERE user_id = ? ORDER BY fecha DESC", (session['user_id'],))
    viajes = cursor.fetchall()
    conn.close()
    return render_template('historial.html', viajes=viajes)

if __name__ == "__main__":
    app.run(debug=True)