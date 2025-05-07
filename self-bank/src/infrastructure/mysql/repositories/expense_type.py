from ....domain.repository.i_repository import CrudProtocol
from typing import Optional, List
from returns.result import Result, Success, Failure
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from .base_repository import BaseRepository
from ....domain.entities.schema import ExpenseType
from ....domain.value_objects.dto import CreateExpenseTypeDto, UpdateExpenseTypeDto, ResExpenseTypeDto

class ExpenseTypeRepository(
    BaseRepository,
    CrudProtocol[CreateExpenseTypeDto, UpdateExpenseTypeDto, ResExpenseTypeDto]
):
    async def create(self, dto: CreateExpenseTypeDto) -> Result[ResExpenseTypeDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                # Ensure that created_at is set explicitly to the current time
                expense_type = ExpenseType(
                    name=dto.name,  # Set the name from the DTO
                    created_at=datetime.now(),  # Set the created_at explicitly
                    updated_at=datetime.now()   # Optionally, set updated_at to the same time initially
                )
                session.add(expense_type)
                await session.commit()
                await session.refresh(expense_type)
                return Success(ResExpenseTypeDto.model_validate(expense_type))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def get(self, id: int) -> Optional[ResExpenseTypeDto]:
        async with await self._db.get_session() as session:
            result = await session.get(ExpenseType, id)
            if result:
                return ResExpenseTypeDto.model_validate(result)
            return None

    async def update(self, id: int, dto: UpdateExpenseTypeDto) -> Result[ResExpenseTypeDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                # Fetch the instance from the database
                instance = await session.get(ExpenseType, id)
                if not instance:
                    return Failure(Exception("ExpenseType not found"))

                # Update attributes only if they are provided in the DTO
                if dto.name is not None:  # Ensure we only update if the name is provided (not None)
                    setattr(instance, 'name', dto.name)

                # Optionally update updated_at to the current timestamp when the asset is updated
                setattr(instance, 'updated_at', datetime.now())

                await session.commit()
                await session.refresh(instance)
                return Success(ResExpenseTypeDto.model_validate(instance))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)


    async def delete(self, id: int) -> Result[bool, Exception]:
        async with await self._db.get_session() as session:
            try:
                instance = await session.get(ExpenseType, id)
                if not instance:
                    return Failure(Exception("ExpenseType not found"))

                await session.delete(instance)
                await session.commit()
                return Success(True)
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def list(self) -> List[ResExpenseTypeDto]:
        async with await self._db.get_session() as session:
            result = await session.execute(select(ExpenseType))
            records = result.scalars().all()
            return [ResExpenseTypeDto.model_validate(r) for r in records]
