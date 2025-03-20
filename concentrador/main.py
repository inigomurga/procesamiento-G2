from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List

app = FastAPI()

# Modelo de datos corregido para Pydantic v2
class DatoGenerador(BaseModel):
    id_generador: int
    potencia_kw: float
    velocidad_viento: float
    temperatura_c: float
    timestamp: str

    # Validadores en Pydantic v2
    @field_validator("potencia_kw")
    def validar_potencia(cls, value):
        if not isinstance(value, (int, float)) or value < 0 or value > 5000:
            raise ValueError("Potencia inválida, debe estar entre 0 y 5000 kW")
        return value

    @field_validator("velocidad_viento")
    def validar_velocidad(cls, value):
        if not isinstance(value, (int, float)) or value < 0 or value > 50:
            raise ValueError("Velocidad del viento inválida, debe estar entre 0 y 50 m/s")
        return value

    @field_validator("temperatura_c")
    def validar_temperatura(cls, value):
        if not isinstance(value, (int, float)) or value < -50 or value > 100:
            raise ValueError("Temperatura inválida, debe estar entre -50°C y 100°C")
        return value

    @field_validator("timestamp")
    def validar_timestamp(cls, value):
        try:
            datetime.fromisoformat(value)  # Verifica que sea un formato ISO válido
        except ValueError:
            raise ValueError("El timestamp no tiene un formato ISO8601 válido")
        return value

# Base de datos temporal (simulación)
datos_generadores: List[DatoGenerador] = []

@app.post("/ingresar_dato")
async def recibir_dato(dato: DatoGenerador):
    try:
        datos_generadores.append(dato)
        return {"mensaje": "Dato recibido correctamente", "total_datos": len(datos_generadores)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error procesando el dato: {str(e)}")

@app.get("/datos")
async def obtener_datos():
    return datos_generadores

@app.get("/promedio")
async def calcular_promedios():
    if not datos_generadores:
        raise HTTPException(status_code=404, detail="No hay datos disponibles")

    promedio_potencia = sum(d.potencia_kw for d in datos_generadores) / len(datos_generadores)
    promedio_viento = sum(d.velocidad_viento for d in datos_generadores) / len(datos_generadores)
    promedio_temp = sum(d.temperatura_c for d in datos_generadores) / len(datos_generadores)

    return {
        "promedio_potencia_kw": promedio_potencia,
        "promedio_velocidad_viento": promedio_viento,
        "promedio_temperatura_c": promedio_temp,
        "total_datos": len(datos_generadores)
    }
