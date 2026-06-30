from fastapi import FastAPI
import models
from database import engine

from adapters.input.api_fastapi import router as pago_router

#inicializamos la aplicacion principal
app = FastAPI(
    title="MiniPay API - Hexagonal",
    description="API de pagos estructurada bajo Arquitectura Hexagonal",
    version="2.0.0"
)

models.Base.metadata.create_all(bind=engine)

app.include_router(pago_router)