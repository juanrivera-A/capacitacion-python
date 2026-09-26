# tests/test_wallet.py
from unittest.mock import MagicMock

import pytest
from hypothesis import given
from hypothesis import strategies as st

from src.modulo03.notifier import EmailService
from src.modulo03.wallet import (
    InsufficientBalanceError,
    InvalidAmountError,
    Wallet,
)


def test_wallet_initial_balance_default():
    wallet = Wallet()
    assert wallet.balance == 0.0


def test_wallet_initial_balance_custom():
    wallet = Wallet(initial_balance=100.0)
    assert wallet.balance == 100.0


def test_wallet_initial_balance_negative_raises_exception():
    with pytest.raises(InvalidAmountError):
        Wallet(initial_balance=-50.0)


def test_deposit_valid_amount():
    wallet = Wallet(initial_balance=50.0)
    wallet.deposit(50.0)
    assert wallet.balance == 100.0


@pytest.mark.parametrize("amount", [0.0, -10.0, -0.01])
def test_deposit_invalid_amount_raises_exception(amount: float):
    wallet = Wallet(initial_balance=50.0)
    with pytest.raises(InvalidAmountError):
        wallet.deposit(amount)


def test_withdraw_valid_amount():
    wallet = Wallet(initial_balance=100.0)
    wallet.withdraw(40.0)
    assert wallet.balance == 60.0


@pytest.mark.parametrize("amount", [0.0, -5.0])
def test_withdraw_invalid_amount_raises_exception(amount: float):
    wallet = Wallet(initial_balance=100.0)
    with pytest.raises(InvalidAmountError):
        wallet.withdraw(amount)


def test_withdraw_insufficient_balance_raises_exception():
    wallet = Wallet(initial_balance=50.0)
    with pytest.raises(InsufficientBalanceError):
        wallet.withdraw(100.0)


@given(
    amount=st.floats(
        min_value=0.01, max_value=1e6, allow_nan=False, allow_infinity=False
    )
)
def test_property_deposit_always_increases_balance(amount: float):
    wallet = Wallet(initial_balance=100.0)
    initial = wallet.balance
    wallet.deposit(amount)
    assert wallet.balance > initial


def test_wallet_deposit_triggers_email_notification():
    mock_notifier = MagicMock(spec=EmailService)
    wallet = Wallet(
        initial_balance=100.0, owner_email="juan@example.com", notifier=mock_notifier
    )
    wallet.deposit(50.0)
    mock_notifier.send_email.assert_called_once_with(
        recipient="juan@example.com",
        subject="Depósito Exitoso",
        body="Se han depositado 50.0. Nuevo saldo: 150.0",
    )


def test_wallet_withdraw_triggers_email_notification():
    mock_notifier = MagicMock(spec=EmailService)
    wallet = Wallet(
        initial_balance=100.0, owner_email="juan@example.com", notifier=mock_notifier
    )
    wallet.withdraw(30.0)
    mock_notifier.send_email.assert_called_once_with(
        recipient="juan@example.com",
        subject="Retiro Exitoso",
        body="Se han retirado 30.0. Nuevo saldo: 70.0",
    )


def test_email_service_real_send_email():
    service = EmailService()
    assert service.send_email("test@example.com", "Asunto", "Cuerpo") is True
