from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List
import logging
import os
import math


# Configurar logs
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "errores.log")
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(filename=LOG_FILE, level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI()

class DatoGenerador(BaseModel):
    id_generador: int
    potencia_kw: float
    velocidad_viento: float
    temperatura_c: float
    timestamp: str

    @field_validator("potencia_kw")
    def validar_potencia(cls, value, values):
        id_gen = values.data.get("id_generador", "Desconocido")
        if not isinstance(value, (int, float)) or value < 0 or value > 5000 or math.isnan(value):
            error_msg = f"[GEN-{id_gen}] Potencia invalida: {value}, debe estar entre 0 y 5000 kW"
            logging.error(error_msg)
            raise ValueError(error_msg)
        return value

    @field_validator("velocidad_viento")
    def validar_velocidad(cls, value, values):
        id_gen = values.data.get("id_generador", "Desconocido")
        if not isinstance(value, (int, float)) or value < 0 or value > 50 or math.isnan(value):
            error_msg = f"[GEN-{id_gen}] Velocidad del viento invalida: {value}, debe estar entre 0 y 50 m/s"
            logging.error(error_msg)
            raise ValueError(error_msg)
        return value

    @field_validator("temperatura_c")
    def validar_temperatura(cls, value, values):
        id_gen = values.data.get("id_generador", "Desconocido")
        if not isinstance(value, (int, float)) or value < -50 or value > 100 or math.isnan(value):
            error_msg = f"[GEN-{id_gen}] Temperatura invalida: {value}, debe estar entre -50 C y 100 C"
            logging.error(error_msg)
            raise ValueError(error_msg)
        return value

datos_generadores: List[DatoGenerador] = []
datos_correctos: List[DatoGenerador] = []
@app.post("/ingresar_dato")
async def recibir_dato(dato: DatoGenerador):
    try:
        datos_generadores.append(dato)
        
        try:
            validado = DatoGenerador(**dato.dict())
            datos_correctos.append(validado)
        except ValueError:
            pass  

        return {"mensaje": "Dato recibido correctamente", "total_datos": len(datos_generadores)}
    
    except Exception as e:
        error_msg = f"Error procesando el dato de ID {dato.id_generador}: {str(e)}"
        logging.error(error_msg)
        raise HTTPException(status_code=400, detail=error_msg)

@app.get("/datos")
async def obtener_datos():
    return datos_generadores  

@app.get("/datos_correctos")
async def obtener_datos_correctos():
    return datos_correctos  

@app.get("/promedio")
async def calcular_promedios():
    if not datos_correctos:
        raise HTTPException(status_code=404, detail="No hay datos válidos disponibles")

    promedio_potencia = sum(d.potencia_kw for d in datos_correctos) / len(datos_correctos)
    promedio_viento = sum(d.velocidad_viento for d in datos_correctos) / len(datos_correctos)
    promedio_temp = sum(d.temperatura_c for d in datos_correctos) / len(datos_correctos)

    return {
        "promedio_potencia_kw": promedio_potencia,
        "promedio_velocidad_viento": promedio_viento,
        "promedio_temperatura_c": promedio_temp,
        "total_datos_validos": len(datos_correctos)
    }
