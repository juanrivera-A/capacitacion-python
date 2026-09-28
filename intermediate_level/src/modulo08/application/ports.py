from typing import Protocol

from ...modulo08.domain.models import Account


class AccountRepositoryPort(Protocol):
    """Puerto (interfaz) para las operaciones de persistencia de cuentas."""

    def save(self, account: Account) -> None: ...

    def get_by_id(self, account_id: str) -> Account | None: ...


class NotificationServicePort(Protocol):
    """Puerto (interfaz) para el servicio de mensajería/notificaciones."""

    def send_notification(self, recipient: str, message: str) -> None: ...
