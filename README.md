# Examen Transversal Programación y Redes Virtualizadas (DRY7122)

## Objetivo
Este repositorio contiene los scripts desarrollados para la evaluación transversal, incluyendo validación de VLANs, interacción con API GraphHopper, gestión de usuarios (SQLite), automatización con NETCONF/RESTCONF y Netmiko hacia routers CSR1000v.

## Dependencias e Instalación
Para instalar todas las librerías necesarias para ejecutar los módulos, corra el siguiente comando en su terminal:
`pip install -r requirements.txt`

## Ejecución de los Módulos
- **Integrantes**: Ejecute `python3 integrantes.py` para visualizar la lista del equipo.
- **VLAN Check**: Ejecute `python3 vlan_check.py` para validar rangos de VLAN (Normal/Extendido).

## Configuración API GraphHopper
Para usar el script de rutas (`ruta_graphhopper.py`), debe crear un archivo oculto llamado `.env` en la raíz del proyecto y agregar su clave así:
`GRAPHHOPPER_API_KEY=su_clave_real_aqui`
*(Se provee un archivo `.env.example` de referencia).*

El script consume dos endpoints:
1. Geocoding API (`/geocode`): Para convertir los nombres de las ciudades a coordenadas (latitud y longitud).
2. Routing API (`/route`): Para calcular la distancia, duración y la narrativa del viaje utilizando las coordenadas obtenidas.

## Configuración API GraphHopper (Ítem 2)
Para ejecutar el script `ruta_graphhopper.py`, es obligatorio contar con una API Key de GraphHopper.
1. Cree un archivo llamado `.env` en la raíz del proyecto.
2. Agregue la siguiente línea: `GRAPHHOPPER_API_KEY=su_clave_real_aqui`
*(Se incluye el archivo `.env.example` en el repositorio para su referencia).*

El script consume los siguientes endpoints de la API:
- **Geocoding API**: Utilizada para transformar los nombres de las ciudades ingresadas en coordenadas geográficas (latitud y longitud).
- **Routing API**: Utilizada para trazar la ruta entre las coordenadas, obteniendo la distancia (km/millas), duración y la narrativa paso a paso.
