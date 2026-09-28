from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ....modulo08.application.dtos import CreateAccountDTO, TransferDTO
from ....modulo08.domain.exceptions import DomainError
from ....modulo08.infrastructure.api.dependencies import UseCasesDep

router = APIRouter(prefix="/accounts", tags=["Accounts"])


class CreateAccountSchema(BaseModel):
    owner_name: str = Field(..., min_length=1)
    initial_balance: float = Field(0.0, ge=0.0)


class TransferSchema(BaseModel):
    source_account_id: str
    destination_account_id: str
    amount: float = Field(..., gt=0.0)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_account(schema: CreateAccountSchema, use_cases: UseCasesDep):
    try:
        dto = CreateAccountDTO(
            owner_name=schema.owner_name,
            initial_balance=schema.initial_balance,
        )
        return use_cases.create_account(dto)
    except DomainError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))


@router.post("/transfer", status_code=status.HTTP_200_OK)
def transfer_funds(schema: TransferSchema, use_cases: UseCasesDep):
    try:
        dto = TransferDTO(
            source_account_id=schema.source_account_id,
            destination_account_id=schema.destination_account_id,
            amount=schema.amount,
        )
        use_cases.transfer(dto)
        return {"message": "Transferencia realizada con éxito."}
    except DomainError as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
