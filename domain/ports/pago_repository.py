from abc import ABC, abstractmethod
from domain.pago import Pago

class PagoRepository(ABC): 

    @abstractmethod
    def guardar(self, pago: Pago) -> Pago:
        pass

    @abstractmethod
    def buscar_por_id(self, pago_id:str) -> Pago:
        pass

        