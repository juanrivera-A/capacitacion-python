class DomainError(Exception):
    """Excepción base para todos los errores de dominio."""


class InvalidAccountBalanceError(DomainError):
    """Ocurre cuando el saldo inicial o final de una cuenta no cumple las reglas."""


class InsufficientFundsError(DomainError):
    """Ocurre cuando se intenta retirar o transferir un monto mayor al saldo disponible."""


class AccountNotFoundError(DomainError):
    """Ocurre cuando no se localiza una cuenta bancaria."""
