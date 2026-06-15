from sqlalchemy import Column, String, Float
from database import Base

class Pago(Base):
    """
    Representa la tabla "Pagos" en la base de datos.
    Cada instancia de esta clase será una fila real en la tabla.
    """
    __tablename__ = "pagos"

    #Definimos las columnas de la tabla
    id = Column(String, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    moneda = Column(String, nullable=False)
    cuenta_origen = Column(String, nullable=False)
    cuenta_destino = Column(String, nullable=False)
    estado = Column(String, nullable=False, default="PENDIENTE")