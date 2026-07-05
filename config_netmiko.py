import os
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

# 1. BUENA PRÁCTICA: Variables separadas (Lectura segura desde .env)
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

# Diccionario de conexión para Netmiko
dispositivo = {
    'device_type': 'cisco_ios',
    'host': env.get("ROUTER_IP", "192.168.56.119"),
    'username': env.get("ROUTER_USER", "cisco"),
    'password': env.get("ROUTER_PASS", "cisco123!"),
    'port': 22,
}

# Configuración de EIGRP Nombrado (AS 100) IPv4 e IPv6 con interfaces pasivas
comandos_configuracion = [
    "ipv6 unicast-routing",
    "router eigrp EXAMEN",
    "address-family ipv4 unicast autonomous-system 100",
    "af-interface default",
    "passive-interface",
    "exit-af-interface",
    "af-interface GigabitEthernet1",
    "no passive-interface",
    "exit-af-interface",
    "exit-address-family",
    "address-family ipv6 unicast autonomous-system 100",
    "af-interface default",
    "passive-interface",
    "exit-af-interface",
    "af-interface GigabitEthernet1",
    "no passive-interface",
    "exit-af-interface",
    "exit-address-family"
]

# 2. BUENA PRÁCTICA: Manejo de errores
try:
    print(f"\n[+] Conectando al router {dispositivo['host']} mediante Netmiko...")
    conexion = ConnectHandler(**dispositivo)
    print("[+] Conexión SSH exitosa.\n")

    print("[+] Enviando configuración de EIGRP Nombrado...")
    salida_config = conexion.send_config_set(comandos_configuracion)
    print(salida_config)
    print("\n[+] Configuración EIGRP aplicada correctamente.")

    print("\n[+] Recopilando información de validación (comandos show)...")
    # Ejecutar comandos show solicitados
    show_eigrp = conexion.send_command("show running-config | section eigrp")
    show_ip = conexion.send_command("show ip interface brief")
    show_ver = conexion.send_command("show version")
    show_run = conexion.send_command("show running-config")

    # 3. BUENA PRÁCTICA: Cierre de conexión
    conexion.disconnect()
    print("[+] Conexión cerrada de forma segura.\n")

    # Guardar las salidas en un archivo de texto
    nombre_archivo = "07_netmiko_validacion.txt"
    with open(nombre_archivo, "w") as f:
        f.write("=== EIGRP CONFIGURATION ===\n" + show_eigrp + "\n\n")
        f.write("=== INTERFACES STATUS ===\n" + show_ip + "\n\n")
        f.write("=== SHOW VERSION (Fragmento inicial) ===\n" + show_ver[:500] + "...\n\n")
        f.write("=== SHOW RUNNING-CONFIG ===\n" + show_run + "\n")
    
    print(f"[+] ¡Toda la información se guardó con éxito en '{nombre_archivo}'!")

except NetmikoAuthenticationException:
    print("[-] Error: Falla de autenticación. Verifica usuario y contraseña.")
except NetmikoTimeoutException:
    print("[-] Error: Tiempo de espera agotado. Verifica la IP y que el router esté encendido.")
except Exception as e:
    print(f"[-] Ocurrió un error inesperado: {e}")
