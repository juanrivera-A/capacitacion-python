class DomainError(Exception):
    """Excepción base para todos los errores de dominio."""


class InvalidOrderError(DomainError):
    """Se lanza cuando un pedido viola alguna regla de negocio."""


class OutOfStockError(DomainError):
    """Se lanza cuando un producto no tiene suficiente stock disponible."""
