import pytest
from unittest.mock import MagicMock
from application.crear_pago_uc import CrearPagoUseCase
from application.dtos.payment_dto import CreatePaymentDTO
from domain.ports.pago_repository import PagoRepository
from domain.ports.notificador import Notificador
from domain.pago import Pago

def test_crear_pago_exitoso_orquesta_correctamente():
    """
    Unit test to verify that the use case successfully orchestrates the flow.
    
    It ensures that the use case receives the data transfer object, instantiates 
    the domain object, persists it through the repository, and sends the 
    corresponding event notification.
    """
    mock_repo = MagicMock(spec=PagoRepository)
    mock_notificador = MagicMock(spec=Notificador)

    expected_payment = Pago("123", 100.0, "USD", "cuenta1", "cuenta2", "PENDIENTE")
    mock_repo.guardar.return_value = expected_payment

    use_case = CrearPagoUseCase(repo=mock_repo, notificador=mock_notificador)

    test_dto = CreatePaymentDTO(
        amount=100.0,
        currency="USD",
        source_account="cuenta1",
        destination_account="cuenta2"
    )

    result = use_case.ejecutar(id="123", dto=test_dto)

    assert result.id == "123"
    assert result.estado == "PENDIENTE"
    mock_repo.guardar.assert_called_once()
    mock_notificador.notificar_pago_creado.assert_called_once_with(expected_payment)

def test_cambiar_estado_invalido_lanza_excepcion():
    """
    Domain pure unit test to verify that state transitions are blocked 
    if the payment transaction status is no longer PENDING.
    """
    pago = Pago("123", 50000.0, "COP", "origen", "destino", estado="APROBADO")
    with pytest.raises(ValueError, match="No se puede cambiar el estado"):
        pago.cambiar_estado("RECHAZADO")