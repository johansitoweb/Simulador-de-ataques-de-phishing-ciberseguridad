from flask import Flask, request, redirect
import sqlite3
import datetime

app = Flask(__name__)

def registrar_clic(id_clic, ip_usuario):
    conexion = sqlite3.connect('phishing.db')
    cursor = conexion.cursor()
    fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO clics (id_clic, ip_usuario, fecha_hora) VALUES (?, ?, ?)", (id_clic, ip_usuario, fecha_hora))
    conexion.commit()
    conexion.close()

@app.route('/actualizar')
def actualizar():
    id_clic = request.args.get('id')
    ip_usuario = request.remote_addr
    registrar_clic(id_clic, ip_usuario)
    return redirect('/advertencia')

@app.route('/advertencia')
def advertencia():
    return "¡Has caído en una simulación de phishing!"

if __name__ == '__main__':
    #Crear la base de datos y la tabla clics si no existen.
    conexion = sqlite3.connect('phishing.db')
    cursor = conexion.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS clics (id_clic TEXT, ip_usuario TEXT, fecha_hora TEXT)")
    conexion.close()
    app.run(debug=True)