from typing import List, Optional
from returns.result import Result
from ...domain.value_objects.dto import (
    CreateAssetDto,
    UpdateAssetDto,
    ResAssetDto
)
from ...domain.repository.i_repository import CrudProtocol


class AssetUseCase:
    def __init__(self, repository: CrudProtocol[CreateAssetDto, UpdateAssetDto, ResAssetDto]):
        self.repository = repository

    async def create_asset(self, dto: CreateAssetDto) -> Result[ResAssetDto, Exception]:
        return await self.repository.create(dto)

    async def get_all_assets(self) -> List[ResAssetDto]:
        return await self.repository.list()

    async def get_asset(self, id: int) -> Optional[ResAssetDto]:
        return await self.repository.get(id)

    async def update_asset(self, id: int, dto: UpdateAssetDto) -> Result[ResAssetDto, Exception]:
        return await self.repository.update(id, dto)

    async def delete_asset(self, id: int) -> Result[bool, Exception]:
        return await self.repository.delete(id)

