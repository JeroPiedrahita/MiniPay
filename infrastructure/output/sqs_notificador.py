from domain.pago import Pago
from domain.ports.notificador import Notificador
from queue_service import QueueService

class SQSNotificador(Notificador):
    def __init__(self):
        self.service = QueueService()

    def notificar_pago_creado(self, pago:Pago) -> str:
        message_id = self.service.enviar_mensaje_pago(
            pago_id =pago.id,
            monto=pago.monto,
            moneda=pago.moneda
        )

        return message_id