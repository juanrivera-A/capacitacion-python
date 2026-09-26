import pytest

from src.modulo06.adapters import LegacyPaymentAdapter, LegacyPaymentGateway
from src.modulo06.service import CheckoutService
from src.modulo06.strategies import (
    fixed_amount_discount,
    no_discount,
    percentage_discount,
)


def test_strategy_discounts():
    price = 100.0

    assert no_discount(price) == 100.0
    assert percentage_discount(20)(price) == 80.0
    assert fixed_amount_discount(15)(price) == 85.0


def test_strategy_invalid_percentage():
    with pytest.raises(ValueError):
        percentage_discount(150)


def test_adapter_integration():
    legacy_sdk = LegacyPaymentGateway()
    adapter = LegacyPaymentAdapter(legacy_sdk)

    assert adapter.process_payment(50.0) is True
    assert adapter.process_payment(-10.0) is False


def test_checkout_service_with_cache_and_adapter():
    legacy_sdk = LegacyPaymentGateway()
    adapter = LegacyPaymentAdapter(legacy_sdk)
    service = CheckoutService(payment_processor=adapter)

    # 1. Probar Checkout exitoso usando estrategia de 10% descuento
    success = service.checkout(
        base_price=100.0, discount_strategy=percentage_discount(10)
    )
    assert success is True

    # 2. Verificar funcionamiento del decorador de caché en calculate_tax
    tax1 = service.calculate_tax(90.0)
    tax2 = service.calculate_tax(90.0)

    assert tax1 == 14.4
    assert tax1 == tax2
    # Verificar que el resultado provino de la caché inspeccionando el dict del decorador
    assert len(service.calculate_tax.cache) == 1  # type: ignore[attr-defined]
