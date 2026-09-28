from ....modulo08.application.ports import AccountRepositoryPort
from ....modulo08.domain.models import Account


class InMemoryAccountRepositoryAdapter(AccountRepositoryPort):
    """Adaptador de infraestructura: Base de datos en memoria para el repositorio de cuentas."""

    def __init__(self) -> None:
        self._storage: dict[str, Account] = {}

    def save(self, account: Account) -> None:
        self._storage[account.account_id] = account

    def get_by_id(self, account_id: str) -> Account | None:
        return self._storage.get(account_id)
