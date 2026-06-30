from sqlalchemy.orm import Session
from domain.pago import Pago
from ports.pago_repository import PagoRepository
import models #Archivo models.py actual

class SQLAlchemyPagoRepository(PagoRepository):
    def __init__(self, db:Session):
        self.db = db

    def guardar(self, pago:Pago) -> Pago:
        #Convertimos la entidad pura de Dominio a un modelo de SQLAlchemy
        pago_db = models.Pago(
            id=pago.id,
            monto=pago.monto,
            moneda=pago.moneda,
            cuenta_origen=pago.cuenta_origen,
            cuenta_destino=pago.cuenta_destino,
            estado=pago.estado
        )
        self.db.add(pago_db)
        self.db.commit()
        self.db.refresh(pago_db)

        #Devolvemos los datos mapeados de vuelta a una entidad de dominio
        return Pago(
            id=pago_db.id,
            monto=pago_db.monto,
            moneda=pago_db.moneda,
            cuenta_origen=pago_db.cuenta_origen,
            cuenta_destidno=pago_db.cuenta_destino,
            estado=pago_db.estado
        )

        def buscar_por_id(self, pago_id:str) -> Pago:
            pago_db = self.db.query(models.Pago).filter(models.Pago.id == pago_id).first()
            if not pago_db:
                return None
            return Pago(
                id = pago_db.id,
                monto = pago_db.monto,
                moneda = pago_db.moneda,
                cuenta_origen = pago_db.cuenta_origen,
                cuenta_destino = pago_db.cuenta_destino,
                estado = pago_db.estado
            )

            