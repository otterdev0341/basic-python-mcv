from typing import List, Optional
from returns.result import Result

from ...domain.value_objects.dto import (
    CreateAssetTypeDto,
    UpdateAssetTypeDto,
    ResAssetTypeDto,
)
from ...domain.repository.i_repository import CrudProtocol


class AssetTypeUseCase:
    def __init__(self, repository: CrudProtocol[CreateAssetTypeDto, UpdateAssetTypeDto, ResAssetTypeDto]):
        self.repository = repository

    async def create_asset_type(
        self, dto: CreateAssetTypeDto
    ) -> Result[ResAssetTypeDto, Exception]:
        return await self.repository.create(dto)

    async def get_asset_type(self, id: int) -> Optional[ResAssetTypeDto]:
        return await self.repository.get(id)

    async def update_asset_type(
        self, id: int, dto: UpdateAssetTypeDto
    ) -> Result[ResAssetTypeDto, Exception]:
        return await self.repository.update(id, dto)

    async def delete_asset_type(self, id: int) -> Result[bool, Exception]:
        return await self.repository.delete(id)

    async def list_asset_types(self) -> List[ResAssetTypeDto]:
        return await self.repository.list()
