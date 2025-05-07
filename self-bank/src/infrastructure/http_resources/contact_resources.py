from ...server import MCPServer
from ...application.usecase.contact_usecase import ContactUseCase
from domain.value_objects.dto import CreateContactDto, ResContactDto, UpdateContactDto
from returns.result import Result
from typing import Optional


def register_contact_resources(mcp: MCPServer, usecase: ContactUseCase):
    @mcp.resource("contact://create")
    async def create(dto: CreateContactDto) -> Result[ResContactDto, Exception]:  # type: ignore[reportUnusedFunction]
        return await usecase.create_contact(dto)

    @mcp.resource("contact://{id}")
    async def get(id: int) -> Optional[ResContactDto]: # type: ignore[reportUnusedFunction]
        return await usecase.get_contact(id)

    @mcp.resource("contact://list")
    async def list_all() -> list[ResContactDto]: # type: ignore[reportUnusedFunction]
        return await usecase.get_all_contacts()

    @mcp.resource("contact://{id}/delete")
    async def delete(id: int) -> Result[bool, Exception]: # type: ignore[reportUnusedFunction]
        return await usecase.delete_contact(id)

    @mcp.resource("contact://{id}")
    async def update(id: int, dto: UpdateContactDto) -> Result[ResContactDto, Exception]: # type: ignore[reportUnusedFunction]
        return await usecase.update_contact(id, dto)