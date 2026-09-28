import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.modulo08.domain.exceptions import (
    InsufficientFundsError,
    InvalidAccountBalanceError,
)
from src.modulo08.domain.models import Account
from src.modulo08.infrastructure.adapters.in_memory_db import (
    InMemoryAccountRepositoryAdapter,
)
from src.modulo08.infrastructure.api.router import router

# 1. PRUEBAS DE DOMINIO (Unidad pura, sin infraestructura)


def test_account_creation_and_business_rules():
    account = Account.create(owner_name="Juan Rivera", initial_balance=1000.0)
    assert account.balance == 1000.0

    account.deposit(500.0)
    assert account.balance == 1500.0

    account.withdraw(300.0)
    assert account.balance == 1200.0


def test_account_withdraw_insufficient_funds_raises_error():
    account = Account.create(owner_name="Juan Rivera", initial_balance=100.0)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(200.0)


def test_invalid_negative_balance_raises_error():
    with pytest.raises(InvalidAccountBalanceError):
        Account(account_id="123", owner_name="Juan Rivera", balance=-50.0)


# 2. PRUEBAS DE CONTRATO (Validación de Adaptadores contra Puertos)


def test_in_memory_repository_contract():
    repo = InMemoryAccountRepositoryAdapter()
    account = Account.create(owner_name="Test User", initial_balance=500.0)

    # Guardar
    repo.save(account)

    # Recuperar
    fetched = repo.get_by_id(account.account_id)
    assert fetched is not None
    assert fetched.account_id == account.account_id
    assert fetched.owner_name == "Test User"
    assert fetched.balance == 500.0


# 3. PRUEBAS END-TO-END (Flujo HTTP vía FastAPI TestClient)


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_e2e_create_accounts_and_transfer(api_client: TestClient):
    # 1. Crear Cuenta Origen
    res_a = api_client.post(
        "/accounts", json={"owner_name": "Cuenta A", "initial_balance": 1000.0}
    )
    assert res_a.status_code == 201
    acc_a_id = res_a.json()["account_id"]

    # 2. Crear Cuenta Destino
    res_b = api_client.post(
        "/accounts", json={"owner_name": "Cuenta B", "initial_balance": 200.0}
    )
    assert res_b.status_code == 201
    acc_b_id = res_b.json()["account_id"]

    # 3. Realizar Transferencia
    res_transfer = api_client.post(
        "/accounts/transfer",
        json={
            "source_account_id": acc_a_id,
            "destination_account_id": acc_b_id,
            "amount": 400.0,
        },
    )
    assert res_transfer.status_code == 200
    assert res_transfer.json()["message"] == "Transferencia realizada con éxito."
