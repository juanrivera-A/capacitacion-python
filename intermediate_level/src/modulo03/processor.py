# src/modulo03/processor.py
from typing import ClassVar

from src.modulo03.gateway import GatewayNetworkError, PaymentGateway


class InvalidCouponError(Exception):
    """Excepción lanzada cuando el código promocional ingresado no es válido."""


class PaymentFailedError(Exception):
    """Excepción lanzada cuando el pago falla tras agotar todos los reintentos."""


class PaymentProcessor:
    DISCOUNTS: ClassVar[dict[str, float]] = {
        "PROMO10": 0.10,
        "PROMO20": 0.20,
    }

    def __init__(
        self, gateway: PaymentGateway | None = None, max_retries: int = 3
    ) -> None:
        self.gateway = gateway or PaymentGateway()
        self.max_retries = max_retries

    def apply_discount(self, amount: float, coupon: str | None = None) -> float:
        if not coupon:
            return amount

        coupon_upper = coupon.upper()
        if coupon_upper not in self.DISCOUNTS:
            raise InvalidCouponError(f"El cupón '{coupon}' no es válido.")

        discount_rate = self.DISCOUNTS[coupon_upper]
        discounted_amount = amount * (1 - discount_rate)
        return max(0.0, discounted_amount)

    def process_payment(
        self, amount: float, card_number: str, coupon: str | None = None
    ) -> bool:
        final_amount = self.apply_discount(amount, coupon)

        for attempt in range(self.max_retries):
            try:
                return self.gateway.charge(final_amount, card_number)
            except GatewayNetworkError:
                if attempt == self.max_retries - 1:
                    raise PaymentFailedError(
                        f"El pago de {final_amount} falló tras {self.max_retries} intentos por error de red."
                    )
        return False
