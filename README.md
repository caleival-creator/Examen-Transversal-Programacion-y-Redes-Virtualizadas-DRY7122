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

## Gestión de Usuarios y Seguridad (Ítem 3)
Para la creación de la base de datos `usuarios.db` y el manejo de credenciales en el script `usuarios_hash.py`, se utilizó la librería nativa `sqlite3`. 

**Algoritmo de Hashing:** Para asegurar que las contraseñas no se almacenen en texto plano, se implementó la librería nativa de Python `hashlib`. Específicamente, se utilizó el algoritmo **SHA-256** (`hashlib.sha256()`). Durante el login, el sistema toma la contraseña ingresada, la vuelve a encriptar en SHA-256 y compara este nuevo hash directamente con el hash almacenado en la base de datos, garantizando así una validación segura de los integrantes.

## Conexión a router CSR1000v con NETCONF (Ítem 4)
Para ejecutar el script `netconf_check.py`, se deben cumplir los siguientes prerrequisitos:
1. **Librerías:** Se requiere la instalación de `ncclient` para manejar la conexión NETCONF sobre SSH.
2. **Puerto:** El script apunta al puerto estándar NETCONF, que es el **830**.
3. **Variables Seguras:** Las credenciales nunca se almacenan en texto plano en el script. Se deben declarar en el archivo `.env` utilizando las variables: `ROUTER_IP`, `ROUTER_PORT`, `ROUTER_USER` y `ROUTER_PASS`.

## Configuraciones desde Postman con RESTCONF (Ítem 5)
El flujo de trabajo automatizado mediante llamadas a la API RESTCONF consistió en tres operaciones principales utilizando el formato JSON y el modelo de datos `ietf-interfaces`:
1. **Borrado (DELETE):** Se eliminó la interfaz Loopback 11 previamente creada.
2. **Creación (PUT):** Se aprovisionó la interfaz Loopback 22 (IP 22.22.22.22/32) incluyendo el parámetro `"enabled": false` en el Body JSON para garantizar que la interfaz se creara en estado de apagado administrativo.
3. **Consulta (GET):** Se solicitó un listado completo del árbol de interfaces para verificar las configuraciones aplicadas, validando a través de los códigos de respuesta HTTP (204, 201 y 200 respectivamente).

## Automatización con Ansible (Ítem 6)
**Explicación de Idempotencia:**
El playbook creado en esta evaluación es completamente **idempotente**. Esto significa que puede ejecutarse múltiples veces de forma segura sin romper la configuración existente. Si el direccionamiento IPv6, el puerto 9999 de Apache o la instalación del servicio ya están aplicados, Ansible detectará el estado actual y arrojará un estado `ok` (sin cambios) en lugar de un `changed`, garantizando la repetibilidad del código en entornos de producción.

## Configuración con Netmiko (Ítem 7)
Para la configuración de EIGRP Nombrado mediante el script `config_netmiko.py`, se cumplieron los siguientes requerimientos:
1. **Dependencias:** Se importó la librería `netmiko` y se utilizó su clase `ConnectHandler` para establecer la conexión SSH programática hacia el router CSR1000v.
2. **Parámetros de conexión:** Se definió un diccionario de dispositivo que extrae las credenciales de forma segura desde el archivo `.env` (`ROUTER_IP`, `ROUTER_USER`, `ROUTER_PASS` y el puerto 22), cumpliendo con las buenas prácticas de no exponer claves en texto plano.
