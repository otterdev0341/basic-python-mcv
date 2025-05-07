from typing import List, Optional
from returns.result import Result, Failure
from ...domain.value_objects.dto import (
    CreateAssetDto,
    UpdateAssetDto,
    ResAssetDto,
    
)
from ...domain.repository.i_repository import CrudProtocol



class AssetUseCase:
    """
    Asset Use Case class that handles all asset-related business operations.
    Following Domain-Driven Design principles to encapsulate business logic.
    """

    def __init__(self, repository: CrudProtocol[CreateAssetDto, UpdateAssetDto, ResAssetDto]):
        """
        Initialize the Asset Use Case with its repository.

        Args:
            repository: Repository implementing the CrudProtocol for Asset operations
        """
        self.repository = repository

    async def create_asset(self, dto: CreateAssetDto) -> Result[ResAssetDto, Exception]:
        """
        Create a new asset in the system.

        Args:
            dto: CreateAssetDto containing name and asset_type_id

        Returns:
            Result[ResAssetDto, Exception]: Success with created asset or Failure with error
        """
        try:
            # Validate asset type exists before creation
            if not await self._validate_asset_type(dto.asset_type_id):
                return Failure(Exception("Invalid asset type specified"))

            return await self.repository.create(dto)
        except Exception as e:
            return Failure(Exception(f"Failed to create asset: {str(e)}"))

    async def get_all_assets(self) -> List[ResAssetDto]:
        """
        Retrieve all assets in the system.

        Returns:
            List[ResAssetDto]: List of all assets
        """
        try:
            return await self.repository.list()
        except Exception as e:
            # Log error and return empty list
            print(f"Error retrieving assets: {str(e)}")
            return []

    async def get_asset(self, id: int) -> Optional[ResAssetDto]:
        """
        Retrieve a specific asset by its ID.

        Args:
            id: Asset ID to retrieve

        Returns:
            Optional[ResAssetDto]: Asset if found, None otherwise
        """
        try:
            return await self.repository.get(id)
        except Exception as e:
            print(f"Error retrieving asset {id}: {str(e)}")
            return None

    async def update_asset(self, id: int, dto: UpdateAssetDto) -> Result[ResAssetDto, Exception]:
        """
        Update an existing asset's information.

        Args:
            id: ID of the asset to update
            dto: UpdateAssetDto containing fields to update

        Returns:
            Result[ResAssetDto, Exception]: Success with updated asset or Failure with error
        """
        try:
            # Validate asset exists
            existing_asset = await self.get_asset(id)
            if not existing_asset:
                return Failure(Exception("Asset not found"))

            # Validate asset type if being updated
            if dto.asset_type_id and not await self._validate_asset_type(dto.asset_type_id):
                return Failure(Exception("Invalid asset type specified"))

            return await self.repository.update(id, dto)
        except Exception as e:
            return Failure(Exception(f"Failed to update asset: {str(e)}"))

    async def delete_asset(self, id: int) -> Result[bool, Exception]:
        """
        Delete an asset if it has no linked transactions.

        Args:
            id: ID of the asset to delete

        Returns:
            Result[bool, Exception]: Success if deleted, Failure with error
        """
        try:
            # Check if asset exists
            existing_asset = await self.get_asset(id)
            if not existing_asset:
                return Failure(Exception("Asset not found"))

            # TODO: Add check for linked transactions before deletion
            # This would require additional repository methods

            return await self.repository.delete(id)
        except Exception as e:
            return Failure(Exception(f"Failed to delete asset: {str(e)}"))

    

    async def _validate_asset_type(self, asset_type_id: int) -> bool:
        """
        Validate if an asset type exists.

        Args:
            asset_type_id: ID of the asset type to validate

        Returns:
            bool: True if asset type exists, False otherwise
        """
        # TODO: Implement asset type validation
        # This would require access to the asset type repository
        return True

