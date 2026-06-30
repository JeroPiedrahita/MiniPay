class Pago:
    def __init__(self,id:str, monto: float, moneda:str, cuenta_origen:str, cuenta_destino: str, estado: str = "PENDIENTE"):

        self.id = id                      #Guarda el ID en ESTE pago
        self.monto = monto                #Guarda el monto en ESTE pago
        self.moneda = moneda              #Guarda la moneda en ESTE pago
        self.cuenta_origen = cuenta_origen
        self.cuenta_destino = cuenta_destino
        self.estado = estado               #Si no nos pasan un estado, por defecto arranca en "PENDIENTE"

    def cambiar_estado(self, nuevo_estado:str):
        #Regla de negocio (invariante)
        estados_validos = ["PENDIENTE", "APROBADO", "RECHAZADO"]
        if nuevo_estado not in estados_validos:
            raise ValueError(f"Estado '{nuevo_estado}' no es un estado valido")

        #self.estado representa el estado ACTUAL en la base de datos
        if self.estado != "PENDIENTE":
            raise ValueError(
                f"No se puede cambiar el estado a {nuevo_estado}."
                f"La transaccion ya se encuentra en un estado final ({self.estado})."
            )

        #Si paso las reglas anteriores, el objeto muta su estado de forma segura
        self.estado = nuevo_estado
