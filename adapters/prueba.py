import uuid

#1. Diccionario (Equivalente a un Struct o un HashMap en C#)
def crear_pago_ficticio(monto: float, moneda: str) -> dict:
    #Generamos un ID único simulando lo que hara la API mas adelante
    pago_id = str(uuid.uuid4())

    #Creamos la estructura llave-valor
    pago = {
        "id": pago_id,
        "monto": monto,
        "moneda": moneda,
        "estado": "PROCESADO"

    }

    return pago


# 2. Lista (Equivalente a un List <T> EN c# o un array dinamico)
transacciones = []

# Agregamos elementos dinamicamente (.append() es como el -Add() en C#)
pago1 = crear_pago_ficticio(150000.0, "COP")
pago2 = crear_pago_ficticio(200.0, "USD")
pago3 = crear_pago_ficticio(85000.0, "COP")

transacciones.append(pago1)
transacciones.append(pago2) 
transacciones.append(pago3)

# 3. Estructura de Control: Loop For-In (Foreach) y Condicional
print("=== Reporte de transacciones del dia===")

for t in transacciones:
    #Python usa f-strings para interpolar variables de forma limpia
    print (f"Transacción {t['id']}: {t['monto']} {t['moneda']} [{t['estado']}]")

    #Condicional simple para simular una alerta bancaria
    if t["moneda"] == "USD" and t["monto"] > 400.0:
        print("Alerta: Transaccion en moneda extranjera requiere revision.")
        