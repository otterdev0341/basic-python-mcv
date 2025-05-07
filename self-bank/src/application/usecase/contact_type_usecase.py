from typing import List, Optional
from returns.result import Result

from ...domain.value_objects.dto import (
    CreateContactTypeDto,
    UpdateContactTypeDto,
    ResContactTypeDto,
)
from ...domain.repository.i_repository import CrudProtocol


class ContactTypeUseCase:
    def __init__(self, repository: CrudProtocol[CreateContactTypeDto, UpdateContactTypeDto, ResContactTypeDto]):
        self.repository = repository

    async def create_contact_type(
        self, dto: CreateContactTypeDto
    ) -> Result[ResContactTypeDto, Exception]:
        return await self.repository.create(dto)

    async def get_contact_type(self, id: int) -> Optional[ResContactTypeDto]:
        return await self.repository.get(id)

    async def update_contact_type(
        self, id: int, dto: UpdateContactTypeDto
    ) -> Result[ResContactTypeDto, Exception]:
        return await self.repository.update(id, dto)

    async def delete_contact_type(self, id: int) -> Result[bool, Exception]:
        return await self.repository.delete(id)

    async def list_contact_types(self) -> List[ResContactTypeDto]:
        return await self.repository.list()
