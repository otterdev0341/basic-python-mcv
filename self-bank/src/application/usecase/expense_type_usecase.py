from typing import Optional, List
from returns.result import Result

from ...domain.value_objects.dto import (
    CreateExpenseTypeDto,
    UpdateExpenseTypeDto,
    ResExpenseTypeDto,
)
from ...domain.repository.i_repository import CrudProtocol


class ExpenseTypeUseCase:
    def __init__(self, repository: CrudProtocol[CreateExpenseTypeDto, UpdateExpenseTypeDto, ResExpenseTypeDto]):
        self.repository = repository

    async def create_expense_type(
        self, dto: CreateExpenseTypeDto
    ) -> Result[ResExpenseTypeDto, Exception]:
        return await self.repository.create(dto)

    async def get_expense_type(self, id: int) -> Optional[ResExpenseTypeDto]:
        return await self.repository.get(id)

    async def update_expense_type(
        self, id: int, dto: UpdateExpenseTypeDto
    ) -> Result[ResExpenseTypeDto, Exception]:
        return await self.repository.update(id, dto)

    async def delete_expense_type(self, id: int) -> Result[bool, Exception]:
        return await self.repository.delete(id)

    async def list_expense_types(self) -> List[ResExpenseTypeDto]:
        return await self.repository.list()
