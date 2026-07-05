import sqlite3
import hashlib
import datetime
from flask import Flask

app = Flask(__name__)
DB_NAME = "usuarios.db"

# Cumple: Crear tabla con campos mínimos exigidos
def inicializar_bd():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            fecha_creacion TEXT NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

# Cumple: Guardar contraseña como hash (no texto plano)
def hashear_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_usuario():
    print("\n--- REGISTRO DE INTEGRANTES ---")
    usuario = input("Ingrese el nombre de usuario (Ej. Carlos / Angello): ")
    password = input("Ingrese la contraseña a registrar: ")
    
    pass_hash = hashear_password(password)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (usuario, password_hash, fecha_creacion) VALUES (?, ?, ?)", 
                       (usuario, pass_hash, fecha))
        conexion.commit()
        print(f"[+] ¡Usuario '{usuario}' registrado con éxito en la base de datos!")
    except sqlite3.IntegrityError:
        print(f"[-] Error: El usuario '{usuario}' ya existe.")
    finally:
        conexion.close()

# Cumple: Validación básica de usuario comparando hash
def validar_usuario():
    print("\n--- LOGIN DE USUARIO ---")
    usuario = input("Ingrese el nombre de usuario: ")
    password = input("Ingrese la contraseña: ")
    
    pass_hash = hashear_password(password)
    
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND password_hash = ?", (usuario, pass_hash))
    resultado = cursor.fetchone()
    conexion.close()
    
    if resultado:
        print(f"[+] ¡Autenticación EXITOSA! Bienvenido al sistema, {usuario}.")
    else:
        print("[-] Autenticación FALLIDA. Credenciales incorrectas.")

@app.route('/')
def index():
    return "<h1>Sitio Web Activo (Examen DEVASC)</h1><p>Sistema de validación en ejecución.</p>"

def iniciar_servidor():
    print("\n[i] Levantando sitio web en el puerto 5800...")
    # Cumple: Sitio web utilizando el puerto 5800
    app.run(host='0.0.0.0', port=5800)

if __name__ == "__main__":
    inicializar_bd() # Genera la Evidencia 2 (usuarios.db)
    while True:
        print("\n" + "="*50)
        print("   GESTIÓN DE USUARIOS, HASH Y SITIO WEB   ")
        print("="*50)
        print("1. Registrar nuevo integrante (Terminal)")
        print("2. Validar usuario (Login en Terminal)")
        print("3. Iniciar Sitio Web (Puerto 5800)")
        print("4. Salir")
        
        opcion = input("\nElija una opción (1-4): ")
        
        if opcion == '1':
            registrar_usuario()
        elif opcion == '2':
            validar_usuario()
        elif opcion == '3':
            iniciar_servidor()
            break # Sale del menú y mantiene el sitio web corriendo
        elif opcion == '4':
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida.")
