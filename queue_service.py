import json
import os
import boto3
from dotenv import load_dotenv

# Cargamos las variables de entorno definidas en el archivo .env
load_dotenv()

class QueueService:
    def __init__(self):
        """
        Inicializa el cliente de AWS SQS utilizando Boto3.
        Recupera las credenciales y la region desde las variables de entorno
        """

        #Extraemos la URL de la cola y la configuracion de AWS
        self.queue_url = os.getenv("SQS_QUEUE_URL")
        region_name = os.getenv("AWS_REGION", "us-east-1")
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        # Inicializamos el cliente de SQS
        # En el dia 4, cuando configuramos Localstack o AWS real, esta misma estructura funcionra
        self.sqs_client = boto3.client(
            "sqs",
            region_name=region_name,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key

        )

    def enviar_mensaje_pago(self, pago_id:str, monto: float, moneda:str):
        """
        Contruye un mensaje en formato JSON con los datos esenciales de la transaccion
        y lo publica en la cola de AWS SQS de forma asincrona para el worker.
        """

        #1. Diseñamos el cuerpo del mensaje  (Carga util o Payload)
        # No mandamos todo el objeto de la base de datos, solo lo necesario para que l worker procese
        cuerpo_mensaje = {
            "pago_id": pago_id,
            "monto": monto,
            "moneda": moneda,
            "evento": "PAGO_CREADO"
        }

        try:
            #2. Despachamos el mensaje a AWS SQS
            # json. dumps() convierte el diccionario de Python en un String JSON plano
            respuesta = self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(cuerpo_mensaje)

            )

            # Retornamos el MessageID que genera AWS para confirmar que la cola lo recibio
            return respuesta.get("MessageId")

        except Exception as e:
            # En produccion, aqui implementarias un sistema de logs corporativos (como CloudWatch)
            print(f"Error critico al enviar mensaje a AWS SQS: {str(e)}")
            #No bloqueamos la API, pero retornamos None para que el endpoint sepa que la cola fallo
            return None

        

