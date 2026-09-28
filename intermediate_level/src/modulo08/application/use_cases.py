from ...modulo08.application.dtos import (
    AccountResponseDTO,
    CreateAccountDTO,
    TransferDTO,
)
from ...modulo08.application.ports import (
    AccountRepositoryPort,
    NotificationServicePort,
)
from ...modulo08.domain.exceptions import AccountNotFoundError
from ...modulo08.domain.models import Account


class BankAccountUseCases:
    """Orquestador de casos de uso para operaciones bancarias."""

    def __init__(
        self,
        repository: AccountRepositoryPort,
        notifier: NotificationServicePort,
    ) -> None:
        self.repository = repository
        self.notifier = notifier

    def create_account(self, dto: CreateAccountDTO) -> AccountResponseDTO:
        """Caso de uso: Crear una nueva cuenta bancaria."""
        account = Account.create(
            owner_name=dto.owner_name,
            initial_balance=dto.initial_balance,
        )
        self.repository.save(account)
        self.notifier.send_notification(
            recipient=account.owner_name,
            message=f"Cuenta creada con éxito. ID: {account.account_id}",
        )
        return AccountResponseDTO(
            account_id=account.account_id,
            owner_name=account.owner_name,
            balance=account.balance,
        )

    def transfer(self, dto: TransferDTO) -> None:
        """Caso de uso: Transferir fondos entre dos cuentas."""
        source_account = self.repository.get_by_id(dto.source_account_id)
        if source_account is None:
            raise AccountNotFoundError(
                f"Cuenta origen no encontrada: {dto.source_account_id}"
            )

        dest_account = self.repository.get_by_id(dto.destination_account_id)
        if dest_account is None:
            raise AccountNotFoundError(
                f"Cuenta destino no encontrada: {dto.destination_account_id}"
            )

        # Ejecución de reglas de negocio en el dominio
        source_account.withdraw(dto.amount)
        dest_account.deposit(dto.amount)

        # Persistencia del nuevo estado
        self.repository.save(source_account)
        self.repository.save(dest_account)

        # Notificación
        self.notifier.send_notification(
            recipient=source_account.owner_name,
            message=f"Transferencia de ${dto.amount} enviada correctamente.",
        )
        self.notifier.send_notification(
            recipient=dest_account.owner_name,
            message=f"Transferencia de ${dto.amount} recibida.",
        )
