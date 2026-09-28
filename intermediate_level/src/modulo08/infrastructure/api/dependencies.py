from typing import Annotated

from fastapi import Depends

from ....modulo08.application.use_cases import BankAccountUseCases
from ....modulo08.infrastructure.adapters.in_memory_db import (
    InMemoryAccountRepositoryAdapter,
)
from ....modulo08.infrastructure.adapters.mock_notifier import (
    MockNotificationAdapter,
)

# Instancias compartidas para mantener estado en memoria durante la ejecución
_repository = InMemoryAccountRepositoryAdapter()
_notifier = MockNotificationAdapter()


def get_use_cases() -> BankAccountUseCases:
    """Proveedor de dependencias (Wiring) que ensambla los adaptadores con los casos de uso."""
    return BankAccountUseCases(repository=_repository, notifier=_notifier)


UseCasesDep = Annotated[BankAccountUseCases, Depends(get_use_cases)]
