from domain.pago import Pago
from domain.ports.pago_repository import PagoRepository
from domain.ports.notificador import Notificador
from application.dtos.payment_dto import CreatePaymentDTO

class CrearPagoUseCase:
    def __init__(self, repo: PagoRepository, notificador: Notificador):
        self.repo = repo
        self.notificador = notificador

    def ejecutar(self, id: str, dto: CreatePaymentDTO) -> Pago:
        """
        Orchestrates the business logic for creating a payment using the provided DTO.
        
        Args:
            id (str): The unique identifier for the payment.
            dto (CreatePaymentDTO): The data transfer object containing payment details.
            
        Returns:
            Pago: The persisted payment domain model.
        """
        new_payment = Pago(
            id=id,
            monto=dto.amount,
            moneda=dto.currency,
            cuenta_origen=dto.source_account,
            cuenta_destino=dto.destination_account,
            estado="PENDIENTE"
        )

        saved_payment = self.repo.guardar(new_payment)
        self.notificador.notificar_pago_creado(saved_payment)

        return saved_payment