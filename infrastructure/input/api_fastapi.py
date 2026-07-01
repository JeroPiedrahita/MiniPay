import uuid
from fastapi import FastAPI, HTTPException, Depends, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from infrastructure import models
from infrastructure.database import get_db
from application.crear_pago_uc import CrearPagoUseCase
from application.payment_dto import CreatePaymentDTO
from infrastructure.outputs.sqlalchemy_repo import SQLAlchemyPagoRepository
from infrastructure.outputs.sqs_notificador import SQSNotificador

router = APIRouter()

class PaymentRequest(BaseModel):
    amount: float = Field(..., gt=0)
    currency: str = Field(..., pattern="^(COP|USD)$")
    source_account: str = Field(..., min_length=5)
    destination_account: str = Field(..., min_length=5)

@router.post("/pago")
async def crear_pago(request: PaymentRequest, db: Session = Depends(get_db)):
    """
    HTTP Input Adapter endpoint for creating payments.
    
    Validates the incoming payload, converts it into an application DTO,
    and executes the usecase workflow.
    """
    payment_id = str(uuid.uuid4())
    repo = SQLAlchemyPagoRepository(db)
    notificador = SQSNotificador()
    use_case = CrearPagoUseCase(repo, notificador)

    application_dto = CreatePaymentDTO(
        amount=request.amount,
        currency=request.currency,
        source_account=request.source_account,
        destination_account=request.destination_account
    )

    try:
        final_payment = use_case.ejecutar(id=payment_id, dto=application_dto)
        return final_payment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")