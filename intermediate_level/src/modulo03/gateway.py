# src/modulo03/gateway.py


class GatewayNetworkError(Exception):
    """Excepción lanzada cuando hay un fallo de red o tiempo de espera en la pasarela"""


class PaymentGateway:
    def charge(self, amount: float, card_number: str) -> bool:
        # En producción, esto se conecta a Stripe/Paypal
        return True
