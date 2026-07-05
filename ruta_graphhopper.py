import requests
import urllib.parse
import os

# 1. Manejo seguro de API Key
def leer_api_key():
    try:
        with open(".env", "r") as f:
            for linea in f:
                if "GRAPHHOPPER_API_KEY" in linea:
                    return linea.split("=")[1].strip()
    except FileNotFoundError:
        return None

API_KEY = leer_api_key()

# 2. Control de error: API Key ausente
if not API_KEY or API_KEY == "tu_clave_de_ejemplo_aqui" or API_KEY == "PEGA_AQUI_TU_CLAVE_REAL":
    print(" [!] Error Crítico: No se encontró una API Key válida. Configure el archivo .env")
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
                # AQUI ESTA LA CORRECCION (["point"]["lat"]):
                return data["hits"][0]["point"]["lat"], data["hits"][0]["point"]["lng"]
            else:
                # 3. Control de error: Ciudad inválida
                print(f" [!] Error: La ciudad '{ciudad}' no existe o no pudo ser localizada.")
        else:
            # 4. Control de error: HTTP Geocoding
            print(f" [!] Error HTTP {res.status_code} en Geocoding: {res.text}")
    except requests.exceptions.RequestException as e:
        print(f" [!] Error de conexión: {e}")
    return None, None

while True:
    print("\n" + "="*60)
    print("       CALCULADORA DE RUTAS INTERNACIONALES       ")
    print("="*60)
    
    origen = input("Ingrese 'Ciudad de Origen' (o presione 's' para salir): ")
    if origen.lower() == 's':
        print("Saliendo de la aplicación...")
        break
        
    destino = input("Ingrese 'Ciudad de Destino' (o presione 's' para salir): ")
    if destino.lower() == 's':
        print("Saliendo de la aplicación...")
        break

    print("\nMedios de transporte: car (Auto), bike (Bicicleta), foot (A pie)")
    vehiculo = input("Elija tipo de medio de transporte a utilizar: ").lower()
    if vehiculo not in ['car', 'bike', 'foot']:
        print("Opción no válida. Se utilizará 'car' por defecto.")
        vehiculo = 'car'

    print("\nCalculando ruta, por favor espere...")
    lat_origen, lng_origen = obtener_coordenadas(origen)
    lat_destino, lng_destino = obtener_coordenadas(destino)

    if not lat_origen or not lat_destino:
        print(" [!] Error: No se puede calcular la ruta debido a parámetros inválidos.")
        continue

    url_ruta = f"{ROUTING_API}?point={lat_origen},{lng_origen}&point={lat_destino},{lng_destino}&profile={vehiculo}&locale=es&key={API_KEY}"
    
    try:
        res_ruta = requests.get(url_ruta)
        if res_ruta.status_code == 200:
            ruta = res_ruta.json()["paths"][0]
            
            dist_km = ruta["distance"] / 1000
            dist_mi = dist_km * 0.621371
            segundos = ruta["time"] / 1000
            horas = int(segundos // 3600)
            minutos = int((segundos % 3600) // 60)
            
            print("\n" + "*"*60)
            print(f" RUTA: {origen.upper()} -> {destino.upper()} ({vehiculo.upper()})")
            print(f" -> Coordenadas Origen : Latitud {lat_origen}, Longitud {lng_origen}")
            print(f" -> Coordenadas Destino: Latitud {lat_destino}, Longitud {lng_destino}")
            print("*"*60)
            print(f"- Distancia de viaje : {dist_km:.2f} Kilómetros / {dist_mi:.2f} Millas")
            print(f"- Duración del viaje : {horas} horas y {minutos} minutos")
            
            print("\n--- NARRATIVA DEL VIAJE ---")
            for paso in ruta["instructions"]:
                print(f"> {paso['text']} ({paso['distance']/1000:.2f} km)")
            print("*"*60 + "\n")
        else:
            print(f" [!] Error HTTP {res_ruta.status_code} al trazar la ruta. Es posible que no exista conexión terrestre para el vehículo seleccionado.")
    except requests.exceptions.RequestException:
         print(" [!] Error crítico de red al solicitar la ruta.")
