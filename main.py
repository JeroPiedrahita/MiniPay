from fastapi import FastAPI, HTTPException
import uuid
from pydantic import BaseModel, Field

#iNICIALIZAMOS LA APLICACION PRINCIPAL
app= FastAPI (
    title= "MiniPay API",
    description= "API para la recepcion y validacion de solicitudes de pago en MiniPay",
    version= "1.0.0"
)

# --- Base de datos simulada en memoria ---
# Este diccionario guardará los pagos usando el 'id' generado como llave
db_pagos = {}

#1. Definicmos el esquema de validacion (Data Transfer Object -DTO)
class PagoRequest(BaseModel):
    #El monto debe ser estrictamente mayor que cer (> 0)
    monto: float = Field(..., gt=0, description= "Monto de la transaccion, debe de ser mayor a cero")

    #La moneda solo puede ser COP o USD utilizando una expresion reular
    moneda: str = Field(..., pattern= "^(COP|USD)$", description= "Moneda de la transaccion, solo se aceptan COP o USD")
    
    cuenta_origen: str = Field(..., min_length=5, description="Numero de cuenta del emisor")
    cuenta_destino: str = Field(..., min_length=5, description="Numero de cuenta del receptor")


#Definimos el endpoint de salud (Heartbeat)
@app.get ("/salud")
async def verificar_salud():
    """
    Endpoint de control para verificar que la API esta en linea.
    Utilizando por balanceadores de carga y sistemas de monitoreo.
    """
    return {"status": "ok"}

#2. Creamos el Endpont POST para recibir el pago
@app.post("/pago")
async def crear_pago(solicitud: PagoRequest):
    """
    Recibe una solicitud de pago, la valida con Pydantic, 
    le asigna un ID unico y la marca con estado "PENDIENTE".
    """
    pago_id = str(uuid.uuid4())

    #Contruimos la respuesta siulando que el objeto ya esta listo
    # .model_dump() convierte el objeto Pydantic de vuelta a un diccionario nativo de python
    nuevo_pago ={
        "id": pago_id,
        "monto": solicitud.monto,
        "moneda":solicitud.moneda,
        "cuenta_origen": solicitud.cuenta_origen,
        "cuenta_destino": solicitud.cuenta_destino,
        "estado": "PENDIENTE"

    }

    #-----Persistencia en memoria---
    #Guardamos el objeto completo en nuestro diccionario global
    db_pagos[pago_id] = nuevo_pago

    return nuevo_pago

# CONSULTA PAGO POR ID
@app.get("/pago/{pago_id}")
async def obtener_pago(pago_id: str):
    """
    Busca una transaccion en la base de datos simulada por su ID.
    Si no la encuentra, dispara un error HTTP 404.
    """

    # bUSCAMOS LA LLAVE DIRECTAMENTE EN EL DICCIONARIO
    if pago_id not in db_pagos:
        #En servicios financieros, el error 404 debe ser explicito
        raise HTTPException(
            status_code=404,
            detail=f"Transaccion con ID {pago_id} no encontrada en el sistema"

        )

    return db_pagos[pago_id]