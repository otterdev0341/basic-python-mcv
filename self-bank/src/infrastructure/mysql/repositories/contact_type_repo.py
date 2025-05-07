from ....domain.repository.i_repository import CrudProtocol
from typing import Optional, List
from returns.result import Result, Success, Failure
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from .base_repository import BaseRepository
from ....domain.entities.schema import ContactType
from ....domain.value_objects.dto import (
    CreateContactTypeDto,
    UpdateContactTypeDto,
    ResContactTypeDto
)


class ContactTypeRepository(
    BaseRepository,
    CrudProtocol[CreateContactTypeDto, UpdateContactTypeDto, ResContactTypeDto]
):
    async def create(self, dto: CreateContactTypeDto) -> Result[ResContactTypeDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                contact_type = ContactType(name=dto.name)
                session.add(contact_type)
                await session.commit()
                await session.refresh(contact_type)
                return Success(ResContactTypeDto.model_validate(contact_type))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def get(self, id: int) -> Optional[ResContactTypeDto]:
        async with await self._db.get_session() as session:
            result = await session.get(ContactType, id)
            if result:
                return ResContactTypeDto.model_validate(result)
            return None

    async def update(self, id: int, dto: UpdateContactTypeDto) -> Result[ResContactTypeDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                instance = await session.get(ContactType, id)
                if not instance:
                    return Failure(Exception("ContactType not found"))

                for field, value in dto.model_dump(exclude_unset=True).items():
                    setattr(instance, field, value)

                await session.commit()
                await session.refresh(instance)
                return Success(ResContactTypeDto.model_validate(instance))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def delete(self, id: int) -> Result[bool, Exception]:
        async with await self._db.get_session() as session:
            try:
                instance = await session.get(ContactType, id)
                if not instance:
                    return Failure(Exception("ContactType not found"))

                await session.delete(instance)
                await session.commit()
                return Success(True)
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def list(self) -> List[ResContactTypeDto]:
        async with await self._db.get_session() as session:
            result = await session.execute(select(ContactType))
            records = result.scalars().all()
            return [ResContactTypeDto.model_validate(r) for r in records]
