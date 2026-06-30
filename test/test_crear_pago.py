import pytest
from unittest.mock import MagicMock
from application.crear_pago_uc import CrearPagoUseCase
from ports.pago_repository import PagoRepository
from ports.notificador import Notificador
from domain.pago import Pago

def test_crear_pago_exitoso_orquesta_correctamente():
    #1. Creamos los Mocks (simuladores) de nuestro Puerto de salida
    mock_repo = MagicMock(spec=PagoRepository)
    mock_notificador = MagicMock(spec=Notificador)

    #2. Configuramos el comportamiento esperado del simulador del repositorio
    #Cuando el caso de uso llame a repo.guardar(), el simulador devolvera el objeto procesado
    pago_esperado = Pago("123", 100.0, "USD", "cuenta1", "cuenta2", "PENDIENTE")
    mock_repo.guardar.return_value = pago_esperado

    # 3. Inicializamos el Caso de Uso inyectando los Mocks
    caso_de_uso = CrearPagoUseCase(repo=mock_repo, notificador=mock_notificador)

    #4. Ejecutamos la accion
    resultado = caso_de_uso.ejecutar(
        id="123",
        monto=100.0,
        moneda="USD",
        cuenta_origen="cuenta1",
        cuenta_destino="cuenta2"
    )

    #5. ASSERTS: Verificaciones estrictas
    assert resultado.id =="123"
    assert resultado.estado =="PENDIENTE"

    #Verificamos contratos: ¿El caso de uso realmente llamo a guardar y notificar?
    mock_repo.guardar.assert_called_once()
    mock_notificador.notificar_pago_creado.assert_called_once_with(pago_esperado)

def test_cambiar_estado_invalido_lanza_excepcion():
    pago = Pago("123", 50000.0, "COP", "origen", "destino", estado="APROBADO")

    #Forzamos la regla de negocio para comprobar que dispare el ValueError esperado
    with pytest.raises(ValueError, match="No se puede cambiar el estado"):
        pago.cambiar_estado("RECHAZADO")