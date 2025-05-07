from typing import Optional, List
from returns.result import Result

from ...domain.value_objects.dto import (
    CreateTransactionDto,
    UpdateTransactionDto,
    ResTransactionDto,
)
from ...domain.repository.i_repository import CrudProtocol


class TransactionUseCase:
    def __init__(
        self,
        repository: CrudProtocol[
            CreateTransactionDto,
            UpdateTransactionDto,
            ResTransactionDto,
        ]
    ):
        self.repository = repository

    async def create_transaction(
        self, dto: CreateTransactionDto
    ) -> Result[ResTransactionDto, Exception]:
        return await self.repository.create(dto)

    async def get_transaction(self, id: int) -> Optional[ResTransactionDto]:
        return await self.repository.get(id)

    async def update_transaction(
        self, id: int, dto: UpdateTransactionDto
    ) -> Result[ResTransactionDto, Exception]:
        return await self.repository.update(id, dto)

    async def delete_transaction(self, id: int) -> Result[bool, Exception]:
        return await self.repository.delete(id)

    async def list_transactions(self) -> List[ResTransactionDto]:
        return await self.repository.list()
