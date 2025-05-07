from ....domain.repository.i_repository import CrudProtocol
from typing import Optional, List
from decimal import Decimal 
from returns.result import Result, Success, Failure
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from .base_repository import BaseRepository
from ....domain.entities.schema import CurrentSheet
from ....domain.value_objects.dto import (
    CreateCurrentSheetDto,
    UpdateCurrentSheetDto,
    ResCurrentSheetDto
)


class CurrentSheetRepository(
    BaseRepository,
    CrudProtocol[CreateCurrentSheetDto, UpdateCurrentSheetDto, ResCurrentSheetDto]
):
    async def create(self, dto: CreateCurrentSheetDto) -> Result[ResCurrentSheetDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                current_sheet = CurrentSheet(
                    asset_id=dto.asset_id,
                    balance=dto.balance
                )
                session.add(current_sheet)
                await session.commit()
                await session.refresh(current_sheet)
                return Success(ResCurrentSheetDto.model_validate(current_sheet))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def get(self, id: int) -> Optional[ResCurrentSheetDto]:
        async with await self._db.get_session() as session:
            result = await session.get(CurrentSheet, id)
            if result:
                return ResCurrentSheetDto.model_validate(result)
            return None

    async def update(self, id: int, dto: UpdateCurrentSheetDto) -> Result[ResCurrentSheetDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                current_sheet = await session.get(CurrentSheet, id)
                if not current_sheet:
                    return Failure(Exception("CurrentSheet not found"))

                if dto.balance is not None:
                    # Use setattr to dynamically set the balance column
                    setattr(current_sheet, 'balance', Decimal(dto.balance))  # Set the balance value as Decimal

                await session.commit()
                await session.refresh(current_sheet)
                return Success(ResCurrentSheetDto.model_validate(current_sheet))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def delete(self, id: int) -> Result[bool, Exception]:
        async with await self._db.get_session() as session:
            try:
                current_sheet = await session.get(CurrentSheet, id)
                if not current_sheet:
                    return Failure(Exception("CurrentSheet not found"))

                await session.delete(current_sheet)
                await session.commit()
                return Success(True)
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def list(self) -> List[ResCurrentSheetDto]:
        async with await self._db.get_session() as session:
            result = await session.execute(select(CurrentSheet))
            records = result.scalars().all()
            return [ResCurrentSheetDto.model_validate(r) for r in records]
