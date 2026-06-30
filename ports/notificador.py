from abc import ABC, abstractmethod
from domain.pago import Pago

class Notificador(ABC):

    @abstractmethod
    def notificar_pago_creado(self, pago: Pago) -> str:
        pass