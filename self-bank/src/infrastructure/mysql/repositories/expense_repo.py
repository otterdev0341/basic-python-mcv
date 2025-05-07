from ....domain.repository.i_repository import CrudProtocol
from typing import Optional, List
from returns.result import Result, Success, Failure
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from .base_repository import BaseRepository
from ....domain.entities.schema import Expense
from ....domain.value_objects.dto import CreateExpenseDto, UpdateExpenseDto, ResExpenseDto
from datetime import datetime

class ExpenseRepository(
    BaseRepository,
    CrudProtocol[CreateExpenseDto, UpdateExpenseDto, ResExpenseDto]
):
    async def create(self, dto: CreateExpenseDto) -> Result[ResExpenseDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                # Ensure that created_at and updated_at are set to the current datetime
                expense = Expense(
                    description=dto.description,
                    expense_type_id=dto.expense_type_id,
                    created_at=datetime.now(),  # Explicitly set created_at to the current datetime
                    updated_at=datetime.now()   # Optionally, set updated_at to the same datetime
                )
                session.add(expense)
                await session.commit()
                await session.refresh(expense)
                return Success(ResExpenseDto.model_validate(expense))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def get(self, id: int) -> Optional[ResExpenseDto]:
        async with await self._db.get_session() as session:
            result = await session.get(Expense, id)
            if result:
                return ResExpenseDto.model_validate(result)
            return None

    async def update(self, id: int, dto: UpdateExpenseDto) -> Result[ResExpenseDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                instance = await session.get(Expense, id)
                if not instance:
                    return Failure(Exception("Expense not found"))

                for field, value in dto.model_dump(exclude_unset=True).items():
                    setattr(instance, field, value)

                await session.commit()
                await session.refresh(instance)
                return Success(ResExpenseDto.model_validate(instance))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def delete(self, id: int) -> Result[bool, Exception]:
        async with await self._db.get_session() as session:
            try:
                instance = await session.get(Expense, id)
                if not instance:
                    return Failure(Exception("Expense not found"))

                await session.delete(instance)
                await session.commit()
                return Success(True)
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def list(self) -> List[ResExpenseDto]:
        async with await self._db.get_session() as session:
            result = await session.execute(select(Expense))
            records = result.scalars().all()
            return [ResExpenseDto.model_validate(r) for r in records]
