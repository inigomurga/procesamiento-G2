from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import List
from datetime import datetime
import statistics

app = FastAPI(title="Concentrador Parque Eólico")

# Almacenamiento temporal de datos válidos
datos_validos = []

class DatoGenerador(BaseModel):
    timestamp: datetime
    id_generador: int
    potencia_kw: float

    ...
    @field_validator("potencia_kw")
    def validar_potencia(cls, v):
        if not (0 <= v <= 500):
            raise ValueError("Potencia fuera de rango (0-500)")
        return v

@app.post("/datos")
def recibir_dato(dato: DatoGenerador):
    datos_validos.append(dato)
    return {"mensaje": "Dato recibido correctamente"}


@app.get("/agregados")
def obtener_agregados():
    if not datos_validos:
        return {"mensaje": "No hay datos aún"}
    
    potencias = [d.potencia_kw for d in datos_validos]
    media_total = round(statistics.mean(potencias), 2)
    
    # Media por generador
    media_por_generador = {}
    for d in datos_validos:
        media_por_generador.setdefault(d.id_generador, []).append(d.potencia_kw)
    
    medias = {f"Generador_{k}": round(statistics.mean(v), 2) for k, v in media_por_generador.items()}
    
    return {
        "media_total_kw": media_total,
        "medias_por_generador": medias,
        "total_datos_recibidos": len(datos_validos)
    }
    
@app.get("/historico")
def ver_datos():
    return datos_validos


@app.get("/")
def root():
    return {"mensaje": "Concentrador operativo"}
