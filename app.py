from flask import Flask, render_template, session, redirect, url_for, request
from taximeter import Taximeter
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "taximeter_secret_key"

taxi = Taximeter()

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

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
    taxi.start_trip()
    return redirect(url_for('index'))

@app.route('/detener', methods=['POST'])
def detener():
    taxi.stop_trip()
    return redirect(url_for('index'))

@app.route('/continuar', methods=['POST'])
def continuar():
    taxi.continue_trip()
    return redirect(url_for('index'))

@app.route('/finalizar', methods=['POST'])
def finalizar():
    taxi.end_trip()
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset():
    taxi.reset()
    return redirect(url_for('index'))

@app.route('/precio')
def precio():
    return str(round(taxi.get_current_fare(), 2))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)