from dataclasses import dataclass


@dataclass(frozen=True)
class CreateAccountDTO:
    """DTO de entrada para la creación de una cuenta."""

    owner_name: str
    initial_balance: float = 0.0


@dataclass(frozen=True)
class AccountResponseDTO:
    """DTO de salida con la representación pública de la cuenta."""

    account_id: str
    owner_name: str
    balance: float


@dataclass(frozen=True)
class TransferDTO:
    """DTO para orquestar una transferencia entre dos cuentas."""

    source_account_id: str
    destination_account_id: str
    amount: float
