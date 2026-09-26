from typing import Protocol


class PaymentProcessorProtocol(Protocol):
    """Interfaz estándar que nuestro sistema espera."""

    def process_payment(self, amount: float) -> bool: ...


class LegacyPaymentGateway:
    """Clase externa/heredada con una interfaz incompatible."""

    def make_transaction(
        self, cost_in_cents: int, currency: str = "USD"
    ) -> dict[str, str | int]:
        if cost_in_cents <= 0:
            return {"status": "FAILED", "code": 400}
        return {"status": "SUCCESS", "code": 200}


class LegacyPaymentAdapter:
    """Adaptador que convierte la interfaz de LegacyPaymentGateway a PaymentProcessorProtocol."""

    def __init__(self, legacy_gateway: LegacyPaymentGateway) -> None:
        self._legacy_gateway = legacy_gateway

    def process_payment(self, amount: float) -> bool:
        # Conversión de pesos/dólares a centavos requeridos por el servicio legacy
        amount_in_cents = int(amount * 100)
        response = self._legacy_gateway.make_transaction(amount_in_cents)
        return response.get("status") == "SUCCESS"
