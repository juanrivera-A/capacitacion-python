# tests/test_payment_processor.py
from unittest.mock import MagicMock

import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.modulo03.gateway import GatewayNetworkError, PaymentGateway
from src.modulo03.processor import (
    InvalidCouponError,
    PaymentFailedError,
    PaymentProcessor,
)


def test_apply_discount_none_or_empty_returns_original_amount():
    processor = PaymentProcessor()
    assert processor.apply_discount(amount=100.0, coupon=None) == 100.0
    assert processor.apply_discount(amount=100.0, coupon="") == 100.0


def test_apply_discount_valid_promo10():
    processor = PaymentProcessor()
    assert processor.apply_discount(amount=100.0, coupon="PROMO10") == 90.0


def test_apply_discount_valid_promo20():
    processor = PaymentProcessor()
    assert processor.apply_discount(amount=200.0, coupon="PROMO20") == 160.0


def test_apply_discount_invalid_coupon_raises_exception():
    processor = PaymentProcessor()
    with pytest.raises(InvalidCouponError):
        processor.apply_discount(amount=100.0, coupon="INVALIDO")


@given(
    amount=st.floats(
        min_value=1.0, max_value=1e6, allow_nan=False, allow_infinity=False
    ),
    coupon=st.sampled_from(["PROMO10", "PROMO20"]),
)
def test_property_discount_always_reduces_price_and_is_non_negative(
    amount: float, coupon: str
):
    processor = PaymentProcessor()
    discounted = processor.apply_discount(amount=amount, coupon=coupon)
    assert discounted < amount
    assert discounted >= 0.0


def test_process_payment_success_on_first_try():
    mock_gateway = MagicMock(spec=PaymentGateway)
    mock_gateway.charge.return_value = True

    processor = PaymentProcessor(gateway=mock_gateway)
    result = processor.process_payment(amount=100.0, card_number="1234")

    assert result is True
    mock_gateway.charge.assert_called_once_with(100.0, "1234")


def test_process_payment_retries_and_succeeds_on_third_try():
    mock_gateway = MagicMock(spec=PaymentGateway)
    mock_gateway.charge.side_effect = [
        GatewayNetworkError("Error 1"),
        GatewayNetworkError("Error 2"),
        True,
    ]

    processor = PaymentProcessor(gateway=mock_gateway)
    result = processor.process_payment(amount=100.0, card_number="1234")

    assert result is True
    assert mock_gateway.charge.call_count == 3


def test_process_payment_fails_after_max_retries_raises_exception():
    mock_gateway = MagicMock(spec=PaymentGateway)
    mock_gateway.charge.side_effect = GatewayNetworkError("Fallo constante")

    processor = PaymentProcessor(gateway=mock_gateway)

    with pytest.raises(PaymentFailedError):
        processor.process_payment(amount=100.0, card_number="1234")

    assert mock_gateway.charge.call_count == 3


def test_process_payment_returns_false_if_no_exception_and_charge_fails():
    mock_gateway = MagicMock(spec=PaymentGateway)
    mock_gateway.charge.return_value = False

    processor = PaymentProcessor(gateway=mock_gateway, max_retries=2)
    result = processor.process_payment(amount=100.0, card_number="1234")

    assert result is False
    assert mock_gateway.charge.call_count == 1


def test_payment_gateway_real_charge():
    gateway = PaymentGateway()
    assert gateway.charge(100.0, "1234") is True


def test_payment_processor_default_gateway():
    processor = PaymentProcessor()
    assert isinstance(processor.gateway, PaymentGateway)


def test_process_payment_with_real_default_gateway():
    processor = PaymentProcessor()
    assert processor.process_payment(100.0, "1234") is True


def test_process_payment_zero_max_retries_returns_false():
    mock_gateway = MagicMock(spec=PaymentGateway)
    processor = PaymentProcessor(gateway=mock_gateway, max_retries=0)

    result = processor.process_payment(amount=100.0, card_number="1234")

    assert result is False
    mock_gateway.charge.assert_not_called()
