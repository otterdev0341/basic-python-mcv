from typing import List, Optional
from returns.result import Result
from ...domain.value_objects.dto import (
    CreateContactDto,
    UpdateContactDto,
    ResContactDto,
)
from ...domain.repository.i_repository import CrudProtocol


class ContactUseCase:
    def __init__(self, repository: CrudProtocol[CreateContactDto, UpdateContactDto, ResContactDto]):
        self.repository = repository

    async def create_contact(
        self, dto: CreateContactDto
    ) -> Result[ResContactDto, Exception]:
        return await self.repository.create(dto)

    async def get_all_contacts(self) -> List[ResContactDto]:
        return await self.repository.list()

    async def update_contact(
        self, id: int, dto: UpdateContactDto
    ) -> Result[ResContactDto, Exception]:
        return await self.repository.update(id, dto)

    async def delete_contact(self, id: int) -> Result[bool, Exception]:
        return await self.repository.delete(id)

    async def get_contact(self, id: int) -> Optional[ResContactDto]:
        return await self.repository.get(id)
