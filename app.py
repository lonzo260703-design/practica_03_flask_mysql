import mysql.connector
from flask import Flask, request, render_template

app = Flask(__name__)

# 🔹 Conexión a MySQL (primero local, luego cambiar a Aiven)
import os
import mysql.connector

def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        ssl_disabled=False
    )



@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    correo = request.form["correo"]
    telefono = request.form["telefono"]

    db = conectar()
    cursor = db.cursor()
    cursor.execute("INSERT INTO clientes (nombre, correo, telefono) VALUES (%s, %s, %s)",
    (nombre, correo, telefono))
    db.commit()
    cursor.close()
    db.close()

    return render_template("mostrar_alumno.html", nombre=nombre, correo=correo, telefono=telefono)

@app.route("/alumnos")
def listar_alumnos():
    db = conectar()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes")
    alumnos = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template("listar_alumnos.html", alumnos=alumnos)

if __name__ == "__main__":
    app.run(debug=True)
