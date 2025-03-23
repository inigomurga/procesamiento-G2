import random
import json
import time
import sys
import requests  # Importamos requests para enviar datos a FastAPI
from datetime import datetime, timezone

# URL del servidor FastAPI
API_URL = "http://localhost:8000/ingresar_dato"  # Ajusta si el servidor está en otra IP

def generar_dato(id_generador: int, prob_error: float = 0.15):
    """Genera un dato sintético para un generador eólico con una probabilidad de error en un solo campo."""
    
    # Datos correctos
    potencia = round(random.uniform(500, 3000), 2)  # kW
    velocidad_viento = round(random.uniform(3, 25), 2)  # m/s
    temperatura = round(random.uniform(10, 90), 2)  # °C
    timestamp = datetime.now(timezone.utc).isoformat()  # Con zona horaria UTC
    
    # Introducir error en un solo campo con probabilidad N
    if random.random() < prob_error:
        campo_erroneo = random.choice(["potencia_kw", "velocidad_viento", "temperatura_c"])
        if campo_erroneo == "potencia_kw":
            potencia = random.choice([-1000, "NaN", 99999])
        elif campo_erroneo == "velocidad_viento":
            velocidad_viento = random.choice([-5, "error", 100])
        elif campo_erroneo == "temperatura_c":
            temperatura = random.choice(["null", -273, 200])
    
    return {
        "id_generador": id_generador,
        "potencia_kw": potencia,
        "velocidad_viento": velocidad_viento,
        "temperatura_c": temperatura,
        "timestamp": timestamp
    }

# Simulación continua
def enviar_datos(id_generador):
    while True:
        dato = generar_dato(id_generador)
        print(json.dumps(dato, indent=2))  # Muestra los datos generados en consola
        
        try:
            # Enviar datos a FastAPI
            response = requests.post(API_URL, json=dato, timeout=5)
            print(f"Respuesta del servidor: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"[GEN-{id_generador}] Error de conexión: {e}")

        time.sleep(2)  # Generar datos cada 2 segundos

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python generador.py <id_generador>")
        sys.exit(1)
    
    id_generador = int(sys.argv[1])
    enviar_datos(id_generador)

