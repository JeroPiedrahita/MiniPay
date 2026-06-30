from domain.pago import Pago
from domain.ports.pago_repository import PagoRepository
from domain.ports.notificador import Notificador


class CrearPagoUseCase:
    def __init__(self, repo: PagoRepository, notificador: Notificador):
        self.repo= repo
        self.notificador = notificador

    def ejecutar(self, id: str, monto: float, moneda: str, cuenta_origen: str, cuenta_destino:str) -> Pago:

        # 1. Instanciamos la entidad pura del dominio
        nuevo_pago = Pago(
            id=id,
            monto=monto,
            moneda=moneda,
            cuenta_origen=cuenta_origen,
            cuenta_destino = cuenta_destino,
            estado="PENDIENTE"
        )

        # 2. Persistimos a través del puerto del repositorio
        pago_guardado = self.repo.guardar(nuevo_pago)

        # 3. Publicamos el evento a traves del puerto del notificador
        self.notificador.notificar_pago_creado(pago_guardado)

        # 4. Retornamos la entidad limpia al adaptador de entrada (FastAPI)
        return pago_guardado