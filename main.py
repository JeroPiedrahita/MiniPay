from fastapi import FastAPI, HTTPException, Depends
import uuid
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

#Importamos la configuracion de nuestra base de datos y los modelos del ORM
import models
from database import engine, get_db

#iNICIALIZAMOS LA APLICACION PRINCIPAL
app= FastAPI (
    title= "MiniPay API",
    description= "API para la recepcion y validacion de solicitudes de pago en MiniPay",
    version= "1.0.0"
)

#---- Creacion Automatica de tablas---
# Este comando le dice a SQLalchemy que cree todas las tablas definidas en models.py
# Si es que aun no existen en el archivo minipay.db
models.Base.metadata.create_all(bind=engine)

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
async def crear_pago(solicitud: PagoRequest, db: Session = Depends(get_db)):
    """
    Recibe una solicitud de pago, la valida con Pydantic, 
    le asigna un ID unico y la marca con estado "PENDIENTE".
    """
    pago_id = str(uuid.uuid4())

    #Contruimos la respuesta siulando que el objeto ya esta listo
    # .model_dump() convierte el objeto Pydantic de vuelta a un diccionario nativo de python
    nuevo_pago = models.Pago(
        id=pago_id,
        monto=solicitud.monto,
        moneda=solicitud.moneda,
        cuenta_origen=solicitud.cuenta_origen,
        cuenta_destino=solicitud.cuenta_destino,
        estado="PENDIENTE"
    )

    # -- OPERACIONES DEL ORM---
    db.add(nuevo_pago)   #1. Le decimos a la sesion que prepare la insercion del objeto
    db. commit()         #2. Guardamos fisicamente los cambios en el archivo minipay.db (Es el COMMIT de SQL)
    db.refresh(nuevo_pago) #3. Refrescamos el objeto para traer cualquier valor calculado por la BD


    return nuevo_pago

# 3. Endpoint GET: Consultar pago real por ID en la Base de Datos
@app.get("/pago/{pago_id}")
async def obtener_pago(pago_id: str, db: Session = Depends(get_db)):
    """
    Busca una transaccion en la base de datos simulada por su ID.
    Si no la encuentra, dispara un error HTTP 404.
    """
    # Explicacion del Query: SELECT * FROM pagos WHERE pagos.id == pago_id LIMIT 1;
    pago_db = db.query(models.Pago).filter(models.Pago.id == pago_id).first()
    
    # Si la consulta devuelve None, significa que el ID no existe en la tabla

    if not pago_db:
        #En servicios financieros, el error 404 debe ser explicito
        raise HTTPException(
            status_code=404,
            detail=f"Transaccion con ID {pago_id} no encontrada en el sistema"

        )

    return pago_db

# Esquema para el body del PATCH
class ActualizarEstadoRequest(BaseModel):
    estado: str = Field(..., pattern="^(PENDIENTE|APROBADO|RECHAZADO)$")

@app.patch("/pago/{pago_id}/estado")
async def actualizar_estado(pago_id: str, body: ActualizarEstadoRequest, db: Session = Depends(get_db)):
    """
    Actualizar el estado de una transacción existente.
    Regla de negocio: Solo se puede modificar transacciones que estén en estado PENDIENTE.
    Flujo: Pendiente -> Aprobado o Pendiente -> Rechazado
    """
    #1. Buscamos el pago en la base de datos
    pago_db = db.query(models.Pago).filter(models.Pago.id == pago_id).first()

    if not pago_db:
        raise HTTPException(status_code=404, detail=f"Transaccion {pago_id} no encontrada")

    #2. Control bancario: Validamos la transicion de estado
    if pago_db.estado != "PENDIENTE":
        raise HTTPException(
            status_code=400,
            detail=f"No se puede cambiar el estado. La transaccion ya se encuentra en un estado final ({pago_db.estado})."

        )
    pago_db.estado = body.estado
    db.commit()
    db.refresh(pago_db)

    return pago_db