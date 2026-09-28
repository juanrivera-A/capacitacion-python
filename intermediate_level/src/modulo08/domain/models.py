import uuid
from dataclasses import dataclass

from ...modulo08.domain.exceptions import (
    InsufficientFundsError,
    InvalidAccountBalanceError,
)


@dataclass
class Account:
    """Entidad de Dominio que representa una cuenta bancaria con sus reglas de negocio."""

    account_id: str
    owner_name: str
    balance: float

    def __post_init__(self) -> None:
        if self.balance < 0:
            raise InvalidAccountBalanceError(
                "El saldo inicial de la cuenta no puede ser negativo."
            )

    @classmethod
    def create(cls, owner_name: str, initial_balance: float = 0.0) -> "Account":
        """Método de fábrica para crear una nueva entidad de cuenta con ID único."""
        return cls(
            account_id=str(uuid.uuid4()),
            owner_name=owner_name,
            balance=initial_balance,
        )

    def deposit(self, amount: float) -> None:
        """Regla de negocio: Depositar un monto positivo en la cuenta."""
        if amount <= 0:
            raise InvalidAccountBalanceError(
                "El monto a depositar debe ser mayor a cero."
            )
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """Regla de negocio: Retirar un monto si hay saldo suficiente."""
        if amount <= 0:
            raise InvalidAccountBalanceError(
                "El monto a retirar debe ser mayor a cero."
            )
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Saldo insuficiente. Saldo disponible: {self.balance}, intento de retiro: {amount}"
            )
        self.balance -= amount
