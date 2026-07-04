import requests
import urllib.parse
import os

# Cumple: Manejo seguro de API Key mediante archivo .env
def leer_api_key():
    try:
        with open(".env", "r") as f:
            for linea in f:
                if "GRAPHHOPPER_API_KEY" in linea:
                    return linea.split("=")[1].strip()
    except FileNotFoundError:
        return None

API_KEY = leer_api_key()

# Cumple: Control de errores básicos (API Key ausente)
if not API_KEY or API_KEY == "tu_clave_falsa_de_ejemplo_aqui":
    print("Error Crítico: No se encontró una API Key válida. Configure el archivo .env")
    exit()

GEOCODING_API = "https://graphhopper.com/api/1/geocode"
ROUTING_API = "https://graphhopper.com/api/1/route"

def obtener_coordenadas(ciudad):
    url = f"{GEOCODING_API}?q={urllib.parse.quote(ciudad)}&key={API_KEY}"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if data.get("hits"):
                return data["hits"][0]["lat"], data["hits"][0]["lng"]
    except requests.exceptions.RequestException:
        print("Error de conexión con la API de Geocoding.")
    return None, None

while True:
    print("\n" + "="*50)
    print("   CALCULADORA DE RUTAS INTERNACIONALES   ")
    print("="*50)
    
    origen = input("Ingrese Ciudad de Origen (o presione 's' para salir): ")
    if origen.lower() == 's':
        break
        
    destino = input("Ingrese Ciudad de Destino (o presione 's' para salir): ")
    if destino.lower() == 's':
        break

    vehiculo = input("Elija transporte (car/bike/foot): ").lower()
    if vehiculo not in ['car', 'bike', 'foot']:
        vehiculo = 'car'

    print("\nObteniendo coordenadas...")
    lat_origen, lng_origen = obtener_coordenadas(origen)
    lat_destino, lng_destino = obtener_coordenadas(destino)

    # Cumple: Control de errores básicos (Origen/Destino inválido)
    if not lat_origen or not lat_destino:
        print("Error: Una de las ciudades ingresadas no es válida o no existe. Intente nuevamente.")
        continue

    url_ruta = f"{ROUTING_API}?point={lat_origen},{lng_origen}&point={lat_destino},{lng_destino}&profile={vehiculo}&locale=es&key={API_KEY}"
    
    try:
        res_ruta = requests.get(url_ruta)
        # Cumple: Control de errores HTTP
        if res_ruta.status_code == 200:
            ruta = res_ruta.json()["paths"][0]
            dist_km = ruta["distance"] / 1000
            dist_mi = dist_km * 0.621371
            segundos = ruta["time"] / 1000
            horas = int(segundos // 3600)
            minutos = int((segundos % 3600) // 60)
            
            print("\n" + "*"*50)
            print(f" RUTA: {origen.upper()} -> {destino.upper()} ({vehiculo.upper()})")
            # Cumple: Mostrar coordenadas en pantalla
            print(f" [!] Coordenadas Origen : Lat {lat_origen}, Lng {lng_origen}")
            print(f" [!] Coordenadas Destino: Lat {lat_destino}, Lng {lng_destino}")
            print("*"*50)
            print(f"- Distancia: {dist_km:.2f} km / {dist_mi:.2f} millas")
            print(f"- Duración : {horas} horas y {minutos} minutos")
            print("\n--- NARRATIVA ---")
            for paso in ruta["instructions"]:
                print(f"> {paso['text']} ({paso['distance']/1000:.2f} km)")
            print("*"*50 + "\n")
        else:
            print(f"Error en la API de Rutas (HTTP {res_ruta.status_code}). Respuesta vacía o ruta imposible.")
    except requests.exceptions.RequestException:
         print("Error crítico de conexión al calcular la ruta.")
