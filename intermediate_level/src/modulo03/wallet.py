# src/modulo03/wallet.py
from .notifier import EmailService


class InvalidAmountError(Exception):
    """Excepción lanzada cuando se intenta operar con un monto menor o igual a cero."""


class InsufficientBalanceError(Exception):
    """Excepción lanzada cuando no hay saldo suficiente para retirar."""


class Wallet:
    def __init__(
        self,
        initial_balance: float = 0.0,
        owner_email: str | None = None,
        notifier: EmailService | None = None,
    ) -> None:
        if initial_balance < 0:
            raise InvalidAmountError("El saldo inicial no puede ser negativo")
        self.balance = initial_balance
        self.owner_email = owner_email
        self.notifier = notifier

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("El monto a depositar debe ser mayor a 0")
        self.balance += amount

        # Notificar si hay un notificador y email configurados
        if self.notifier and self.owner_email:
            self.notifier.send_email(
                recipient=self.owner_email,
                subject="Depósito Exitoso",
                body=f"Se han depositado {amount}. Nuevo saldo: {self.balance}",
            )

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise InvalidAmountError("El monto a retirar debe ser mayor a 0")
        if amount > self.balance:
            raise InsufficientBalanceError("Saldo insuficiente para realizar el retiro")
        self.balance -= amount

        # Notificar si hay un notificador y email configurados
        if self.notifier and self.owner_email:
            self.notifier.send_email(
                recipient=self.owner_email,
                subject="Retiro Exitoso",
                body=f"Se han retirado {amount}. Nuevo saldo: {self.balance}",
            )
