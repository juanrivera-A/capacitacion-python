from collections.abc import Callable

from ..modulo06.adapters import PaymentProcessorProtocol
from ..modulo06.decorators import memoize_cache
from ..modulo06.strategies import no_discount


class CheckoutService:
    """Servicio que integra las estrategias de precio, caché y procesamiento de pago."""

    def __init__(self, payment_processor: PaymentProcessorProtocol) -> None:
        self.payment_processor = payment_processor

    @memoize_cache
    def calculate_tax(self, amount: float, tax_rate: float = 0.16) -> float:
        """Simulación de un cálculo costoso protegido por el decorador de caché."""
        return round(amount * tax_rate, 2)

    def checkout(
        self,
        base_price: float,
        discount_strategy: Callable[[float], float] = no_discount,
    ) -> bool:
        discounted_price = discount_strategy(base_price)
        tax = self.calculate_tax(discounted_price)
        total = discounted_price + tax
        return self.payment_processor.process_payment(total)
