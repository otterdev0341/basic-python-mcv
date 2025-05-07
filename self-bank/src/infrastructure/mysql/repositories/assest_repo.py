from ....domain.repository.i_repository import CrudProtocol
from typing import Optional, List
from returns.result import Result, Success, Failure
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from .base_repository import BaseRepository
from ....domain.entities.schema import Asset
from ....domain.value_objects.dto import CreateAssetDto, UpdateAssetDto, ResAssetDto
from datetime import datetime

class AssetRepository(
    BaseRepository,
    CrudProtocol[CreateAssetDto, UpdateAssetDto, ResAssetDto]
):
    async def create(self, dto: CreateAssetDto) -> Result[ResAssetDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                # Ensure the created_at field is set explicitly
                asset = Asset(name=dto.name, asset_type_id=dto.asset_type_id, created_at=datetime.now())
                session.add(asset)
                await session.commit()
                await session.refresh(asset)
                return Success(ResAssetDto.model_validate(asset))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def get(self, id: int) -> Optional[ResAssetDto]:
        async with await self._db.get_session() as session:
            result = await session.get(Asset, id)
            if result:
                return ResAssetDto.model_validate(result)
            return None

    async def update(self, id: int, dto: UpdateAssetDto) -> Result[ResAssetDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                instance = await session.get(Asset, id)
                if not instance:
                    return Failure(Exception("Asset not found"))

                if dto.name:
                    setattr(instance, 'name', dto.name)  # Use setattr to set the value
                if dto.asset_type_id:
                    setattr(instance, 'asset_type_id', dto.asset_type_id)  # Use setattr to set the value

                await session.commit()
                await session.refresh(instance)
                return Success(ResAssetDto.model_validate(instance))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def delete(self, id: int) -> Result[bool, Exception]:
        async with await self._db.get_session() as session:
            try:
                instance = await session.get(Asset, id)
                if not instance:
                    return Failure(Exception("Asset not found"))

                await session.delete(instance)
                await session.commit()
                return Success(True)
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def list(self) -> List[ResAssetDto]:
        async with await self._db.get_session() as session:
            result = await session.execute(select(Asset))
            records = result.scalars().all()
            return [ResAssetDto.model_validate(r) for r in records]
