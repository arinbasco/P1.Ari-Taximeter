# 🚕 Proyecto Python: Taxímetro Digital

## 📝 Descripción del proyecto

Este proyecto consiste en desarrollar un prototipo de taxímetro digital utilizando Python. El objetivo es modernizar el sistema de facturación de los taxis y crear un sistema que calcule las tarifas a cobrar a los clientes de manera precisa y eficiente.

El proyecto se estructura en cuatro niveles incrementales, desde una interfaz por línea de comandos hasta una aplicación web con autenticación y base de datos.



---

## 📋 Gestión del proyecto

Tablero Kanban utilizado para la organización y seguimiento del desarrollo:

🔗 [Tablero del proyecto en Trello] (https://trello.com/invite/b/69fa5279b65fa26b24705875/ATTI2d306c0bfff209e6a67f025c2ea5742e6D96E621/proyecto-taximetro)

---

## 📊 Niveles de implementación

### 🟢 Nivel Esencial — completado

Programa CLI (Interfaz de Línea de Comandos) en Python:

- ✅ Bienvenida y explicación del funcionamiento al iniciar
- ✅ Iniciar un trayecto
- ✅ Calcular tarifa mientras el taxi está parado (2 céntimos por segundo)
- ✅ Calcular tarifa mientras el taxi está en movimiento (5 céntimos por segundo)
- ✅ Finalizar un trayecto y mostrar el total en euros
- ✅ Permitir iniciar un nuevo trayecto sin cerrar el programa

### 🟡 Nivel Medio — completado

- ✅ Sistema de logs para la trazabilidad del código
- ✅ Tests unitarios con pytest (14 tests cubriendo el flujo completo)
- ✅ Registro histórico de trayectos pasados en un archivo de texto plano
- ✅ Configuración de precios modificable durante la ejecución

### 🟠 Nivel Avanzado — parcialmente completado

- ✅ Refactorización del código a Programación Orientada a Objetos (clase `Taximeter`)
- ✅ Sistema de autenticación con contraseñas en la versión CLI (registro e inicio de sesión)
### 🟠 Nivel Avanzado — completado

- ✅ Refactorización del código a Programación Orientada a Objetos (clase `Taximeter`)
- ✅ Sistema de autenticación con contraseñas en la versión CLI (registro e inicio de sesión)
- ✅ Interfaz gráfica de usuario (GUI con Tkinter) implementada con funcionalidad completa, aunque con un tratamiento visual básico

### 🔴 Nivel Experto — parcialmente completado

- ✅ Base de datos SQLite para almacenar usuarios y registros de trayectos
- ✅ Versión web desarrollada con Flask, accesible desde el navegador
- ✅ Login con hash de contraseñas usando bcrypt
- ✅ Sesiones de usuario gestionadas por Flask
- ✅ Visualización del precio en tiempo real con JavaScript
- ✅ Modificación de tarifas desde la interfaz web con confirmación
- ✅ Historial de viajes filtrado por usuario
- ✅ Pantalla de resumen al finalizar el viaje con desglose por subtotales
- ✅ Diseño visual propio con identidad de marca
- ⚠️ **Registro de nuevos usuarios disponible solo en la versión CLI, no en la web por falta de tiempo**
- ⬜ Funcionalidad "Recordarme" en el login no implementada
- ❌ **Dockerización de la aplicación — no realizada**

---

## 🎨 Diseño visual

La versión web tiene una identidad visual propia inspirada en los tickets reales de taxi:

- Paleta de papel crema (`#F2EDE2`), tinta negra y acento naranja (`#E8390E`)
- Tipografías Bebas Neue para títulos, Barlow para textos y Share Tech Mono para datos numéricos
- Bordes perforados que evocan los rollos de impresoras térmicas
- Subtotales formateados como un recibo real, con líneas punteadas y sello "PAGADO"

El CSS fue desarrollado por la IA siguiendo una guía estética propia.

---

## 🛠️ Tecnologías utilizadas

- **Python 3**
- **Flask** — framework web para la versión experto
- **SQLite** — base de datos relacional
- **bcrypt** — hash seguro de contraseñas
- **pytest** — testing unitario
- **HTML / CSS / JavaScript** — interfaz web
- **Git y GitHub** — control de versiones
- **Tablero Kanban** — gestión del proyecto

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Factoria-F5-madrid/project-py-taximetro.git
cd project-py-taximetro

# Crear entorno virtual
python -m venv .taximetro

# Activar entorno virtual (Windows / Git Bash)
source .taximetro/Scripts/activate

# Activar entorno virtual (Linux / Mac)
source .taximetro/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## ▶️ Uso

### Versión CLI

```bash
python taximeter.py
```

Menú interactivo. Desde aquí se puede registrar un nuevo usuario, iniciar sesión, iniciar y finalizar trayectos, modificar tarifas y consultar el historial.

### Versión web

```bash
python app.py
```

Abrir el navegador en:

```
http://127.0.0.1:5000
```

> **Nota importante:** la versión web no incluye el registro de nuevos usuarios. Para crear una cuenta, ejecutá primero la versión CLI y registrá el usuario desde ahí. Una vez creado, podés ingresar con esas credenciales en la versión web.

---

## 🧪 Tests

```bash
pytest test_taximeter.py -v
```

Los 14 tests cubren: inicio de viaje, cálculo de tarifas en distintos estados, transiciones entre detenido y en movimiento, modificación de tarifas y finalización del viaje.

---

## 📁 Estructura del proyecto

```
project-py-taximetro/
├── taximeter.py          # Lógica principal (clase Taximeter)
├── app.py                # Aplicación Flask
├── test_taximeter.py     # Tests unitarios
├── tarifas.txt           # Tarifas persistentes
├── taximeter.db          # Base de datos SQLite (usuarios y viajes)
├── requirements.txt      # Dependencias del proyecto
├── static/
│   └── style.css         # Hoja de estilos
└── templates/
    ├── index.html        # Pantalla principal del taxímetro
    ├── login.html        # Acceso de usuarios
    ├── tarifas.html      # Modificación de precios
    ├── historial.html    # Listado de viajes anteriores
    └── resumen.html      # Ticket de viaje finalizado
```

---

## ⚠️ Pendientes y limitaciones conocidas

- Registro de nuevos usuarios solo disponible en la versión CLI
- Opción "Recordarme" en el login no implementada
- Aplicación no dockerizada


---

Proyecto desarrollado durante el bootcamp de Factoría F5 (Madrid, 2026).