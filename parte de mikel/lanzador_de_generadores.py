import multiprocessing
import random
import time
import datetime
import requests  # lo usaremos más adelante

# Configuración general
PROB_ERROR = 0.1
INTERVALO_SEGUNDOS = 1
URL_CONCENTRADOR = "http://localhost:8000/datos"

def generar_dato_valido():
    return round(random.uniform(50, 150), 2)

def generar_dato_erroneo():
    tipo_error = random.choice(["negativo", "nan", "texto", "fuera_rango"])
    if tipo_error == "negativo":
        return -random.uniform(1, 100)
    elif tipo_error == "nan":
        return float('nan')
    elif tipo_error == "texto":
        return "potencia_invalida"
    elif tipo_error == "fuera_rango":
        return random.uniform(1000, 2000)
    return 0

def crear_dato(id_generador):
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if random.random() < PROB_ERROR:
        potencia = generar_dato_erroneo()
    else:
        potencia = generar_dato_valido()
    return {
        "timestamp": timestamp,
        "id_generador": id_generador,
        "potencia_kw": potencia
    }

def generador(id_generador):
    while True:
        dato = crear_dato(id_generador)
        print(f"[Generador {id_generador}] Dato: {dato}")
        try:
            response = requests.post(URL_CONCENTRADOR, json=dato)
            print(f"[Generador {id_generador}] Respuesta: {response.status_code}")
        except Exception as e:
            print(f"[Generador {id_generador}] Error al enviar: {e}")
        time.sleep(INTERVALO_SEGUNDOS)

if __name__ == "__main__":
    procesos = []
    for i in range(1, 11):  # Generadores 1 a 10
        p = multiprocessing.Process(target=generador, args=(i,))
        procesos.append(p)
        p.start()
    
    # Esperar a que terminen (nunca lo harán, es bucle infinito)
    for p in procesos:
        p.join()
