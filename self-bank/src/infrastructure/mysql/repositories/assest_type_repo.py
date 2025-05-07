from ....domain.repository.i_repository import CrudProtocol
from typing import Optional, List
from returns.result import Result, Success, Failure
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from .base_repository import BaseRepository
from ....domain.entities.schema import AssetType
from ....domain.value_objects.dto import CreateAssetTypeDto, UpdateAssetTypeDto, ResAssetTypeDto


class AssetTypeRepository(
    BaseRepository,
    CrudProtocol[CreateAssetTypeDto, UpdateAssetTypeDto, ResAssetTypeDto]
):
    async def create(self, dto: CreateAssetTypeDto) -> Result[ResAssetTypeDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                asset_type = AssetType(name=dto.name)
                session.add(asset_type)
                await session.commit()
                await session.refresh(asset_type)
                return Success(ResAssetTypeDto.model_validate(asset_type))  # Use model_validate here
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def get(self, id: int) -> Optional[ResAssetTypeDto]:
        async with await self._db.get_session() as session:
            result = await session.get(AssetType, id)
            if result:
                return ResAssetTypeDto.model_validate(result)  # Use model_validate here
            return None

    async def update(self, id: int, dto: UpdateAssetTypeDto) -> Result[ResAssetTypeDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                # Get the existing AssetType from DB
                instance = await session.get(AssetType, id)
                if not instance:
                    return Failure(Exception("Not found"))

                # Check if the name is not None and update
                if dto.name is not None:
                    # Force the type checker to understand that this is valid
                    instance.__setattr__('name', dto.name)  # Explicitly using __setattr__

                # Commit changes to the database
                await session.commit()
                await session.refresh(instance)
                return Success(ResAssetTypeDto.model_validate(instance))  # Use model_validate here
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def delete(self, id: int) -> Result[bool, Exception]:
        async with await self._db.get_session() as session:
            try:
                instance = await session.get(AssetType, id)
                if not instance:
                    return Failure(Exception("Not found"))

                await session.delete(instance)
                await session.commit()
                return Success(True)
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def list(self) -> List[ResAssetTypeDto]:
        async with await self._db.get_session() as session:
            result = await session.execute(select(AssetType))
            records = result.scalars().all()
            return [ResAssetTypeDto.model_validate(r) for r in records]  # Use model_validate here
