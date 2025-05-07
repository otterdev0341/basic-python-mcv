from typing import Optional, List
from returns.result import Result

from ...domain.value_objects.dto import (
    CreateExpenseDto,
    UpdateExpenseDto,
    ResExpenseDto,
)
from ...domain.repository.i_repository import CrudProtocol


class ExpenseUseCase:
    def __init__(self, repository: CrudProtocol[CreateExpenseDto, UpdateExpenseDto, ResExpenseDto]):
        self.repository = repository

    async def create_expense(
        self, dto: CreateExpenseDto
    ) -> Result[ResExpenseDto, Exception]:
        return await self.repository.create(dto)

    async def get_expense(self, id: int) -> Optional[ResExpenseDto]:
        return await self.repository.get(id)

    async def update_expense(
        self, id: int, dto: UpdateExpenseDto
    ) -> Result[ResExpenseDto, Exception]:
        return await self.repository.update(id, dto)

    async def delete_expense(self, id: int) -> Result[bool, Exception]:
        return await self.repository.delete(id)

    async def list_expenses(self) -> List[ResExpenseDto]:
        return await self.repository.list()
