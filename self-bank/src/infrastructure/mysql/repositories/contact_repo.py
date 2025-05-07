from ....domain.repository.i_repository import CrudProtocol
from typing import Optional, List
from returns.result import Result, Success, Failure
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from .base_repository import BaseRepository
from ....domain.entities.schema import Contact
from ....domain.value_objects.dto import (
    CreateContactDto,
    UpdateContactDto,
    ResContactDto
)


class ContactRepository(
    BaseRepository,
    CrudProtocol[CreateContactDto, UpdateContactDto, ResContactDto]
):
    async def create(self, dto: CreateContactDto) -> Result[ResContactDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                contact = Contact(
                    name=dto.name,
                    business_name=dto.business_name,
                    phone=dto.phone,
                    description=dto.description,
                    contact_type_id=dto.contact_type_id
                )
                session.add(contact)
                await session.commit()
                await session.refresh(contact)
                return Success(ResContactDto.model_validate(contact))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def get(self, id: int) -> Optional[ResContactDto]:
        async with await self._db.get_session() as session:
            result = await session.get(Contact, id)
            if result:
                return ResContactDto.model_validate(result)
            return None

    async def update(self, id: int, dto: UpdateContactDto) -> Result[ResContactDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                contact = await session.get(Contact, id)
                if not contact:
                    return Failure(Exception("Contact not found"))

                for field, value in dto.model_dump(exclude_unset=True).items():
                    setattr(contact, field, value)

                await session.commit()
                await session.refresh(contact)
                return Success(ResContactDto.model_validate(contact))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def delete(self, id: int) -> Result[bool, Exception]:
        async with await self._db.get_session() as session:
            try:
                contact = await session.get(Contact, id)
                if not contact:
                    return Failure(Exception("Contact not found"))

                await session.delete(contact)
                await session.commit()
                return Success(True)
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def list(self) -> List[ResContactDto]:
        async with await self._db.get_session() as session:
            result = await session.execute(select(Contact))
            records = result.scalars().all()
            return [ResContactDto.model_validate(r) for r in records]
