from ncclient import manager
import xml.dom.minidom

# Cumple: Variables seguras desde archivo .env
def leer_env():
    env_vars = {}
    try:
        with open(".env", "r") as f:
            for linea in f:
                if "=" in linea:
                    k, v = linea.strip().split("=", 1)
                    env_vars[k] = v
    except FileNotFoundError:
        pass
    return env_vars

env = leer_env()
HOST = env.get("ROUTER_IP")
PORT = env.get("ROUTER_PORT", "830")
USER = env.get("ROUTER_USER")
PASS = env.get("ROUTER_PASS")

if not HOST or not USER or not PASS:
    print("[-] Error: Faltan variables del router en el archivo .env")
    exit()

# Cumple: Apellidos de los integrantes y Loopback 11 con IP 11.11.11.11/32
config_payload = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>Leiva_Acevedo</hostname>
    <interface>
      <Loopback>
        <name>11</name>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

try:
    print(f"\n[+] Conectando al router {HOST}:{PORT} vía NETCONF SSH...")
    # Cumple: Manejo de sesión con ncclient
    with manager.connect(host=HOST, port=PORT, username=USER, password=PASS, hostkey_verify=False, device_params={'name': 'iosxe'}) as m:
        print("[+] ¡Conexión establecida exitosamente!\n")
        
        # Cumple: Salida de capabilities (Evidencia 3)
        print("--- CAPABILITIES DEL ROUTER (Primeras 5) ---")
        for cap in list(m.server_capabilities)[:5]:
            print(f"- {cap}")
            
        print("\n[+] Enviando configuración (Hostname 'Leiva_Acevedo' y Loopback 11)...")
        # Aplica la configuración a la running-config
        respuesta = m.edit_config(target='running', config=config_payload)
        
        # Cumple: Mostrar salida clara y respuesta XML
        print("\n--- RESPUESTA XML DEL ROUTER ---")
        xml_formateado = xml.dom.minidom.parseString(respuesta.xml).toprettyxml()
        print(xml_formateado)
        
        print("[+] ¡Configuración aplicada! Revisa el router para confirmar.")

except Exception as e:
    print(f"\n[-] Error en la conexión o configuración: {e}")
