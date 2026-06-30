import uuid
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

import models
from database import get_db

#Importaciones Hexagonales
from application.crear_pago_uc import CrearPagoUseCase
from adapters.out.sqlalchemy_repo import SQLAlchemyPagoRepository
from adapters.out.sqs_notificador import SQSNotificador


router = APIRouter()

#Esquema de validacion HTTP (DTO de Entrada)
class PagoRequest(BaseModel):
    monto: float = Field(..., gt=0)
    moneda: str = Field(..., pattern="^(COP|USD)$")
    cuenta_origen:str = Field(..., min_length=5)
    cuenta_destino: str = Field(..., min_length=5)

@router.get("/salud")
async def verificar_salud():
    return {"status": "ok"}

@router.post("/pago")
async def crear_pago(solicitud: PagoRequest, db: Session = Depends(get_db)):
    pago_id = str(uuid.uuid4())

    #1. Instanciamos los adaptadores de salida con la infraestructura real
    repo = SQLAlchemyPagoRepository(db)
    notificador = SQSNotificador()

    #2. Inicializamos el caso de uso inyectandole sus dependencias por puerto
    caso_de_uso = CrearPagoUseCase(repo, notificador)

    try:
        #3. Ejecutamos la logica central del sistema
        pago_final = caso_de_uso.ejecutar(
            id=pago.id,
            monto=solicitud.monto,
            moneda=solicitud.moneda,
            cuenta_origen=solicitud.cuenta_origen,
            cuenta_destino=solicitud.cuenta_destino
        )

        return pago_final
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno en el caso de uso: {str(e)}")