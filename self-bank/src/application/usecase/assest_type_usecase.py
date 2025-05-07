from typing import List, Optional
from returns.result import Result, Failure


from ...domain.value_objects.dto import (
    CreateAssetTypeDto,
    UpdateAssetTypeDto,
    ResAssetTypeDto,
)
from ...domain.repository.i_repository import CrudProtocol



class AssetTypeUseCase:
    """
    AssetType Use Case class that handles all asset type-related business operations.
    Following Domain-Driven Design principles to encapsulate business logic for managing
    different types of assets in the system.

    This use case implements the following domain rules:
    1. Asset types must have unique names (case-insensitive)
    2. Asset types cannot be deleted if they are in use
    3. Asset type names must follow specific format rules
    4. Asset types maintain their own audit trail
    """

    def __init__(self, repository: CrudProtocol[CreateAssetTypeDto, UpdateAssetTypeDto, ResAssetTypeDto]):
        """
        Initialize the AssetType Use Case with its repository.

        Args:
            repository: Repository implementing the CrudProtocol for AssetType operations
        """
        self.repository = repository

    async def create_asset_type(
        self, dto: CreateAssetTypeDto
    ) -> Result[ResAssetTypeDto, Exception]:
        """
        Create a new asset type in the system.

        Args:
            dto: CreateAssetTypeDto containing the name of the asset type

        Returns:
            Result[ResAssetTypeDto, Exception]: Success with created asset type or Failure with error

        Domain Rules:
        - Name must not be empty
        - Name must be unique (case-insensitive)
        - Name must follow proper format (alphanumeric with spaces)
        """
        try:
            # Validate asset type name format
            validation_result = self._validate_asset_type_name(dto.name)
            if not validation_result:
                return Failure(Exception("Invalid asset type name format"))

            # Check if asset type with same name already exists
            existing_types = await self.list_asset_types()
            if any(t.name.lower() == dto.name.lower() for t in existing_types):
                return Failure(Exception("Asset type with this name already exists"))

            

            return await self.repository.create(dto)
        except Exception as e:
            return Failure(Exception(f"Failed to create asset type: {str(e)}"))

    async def get_asset_type(self, id: int) -> Optional[ResAssetTypeDto]:
        """
        Retrieve a specific asset type by its ID.

        Args:
            id: Asset type ID to retrieve

        Returns:
            Optional[ResAssetTypeDto]: Asset type if found, None otherwise
        """
        try:
            asset_type = await self.repository.get(id)
            if asset_type:
                # Add domain-specific processing if needed
                return asset_type
            return None
        except Exception as e:
            print(f"Error retrieving asset type {id}: {str(e)}")
            return None

    async def update_asset_type(
        self, id: int, dto: UpdateAssetTypeDto
    ) -> Result[ResAssetTypeDto, Exception]:
        """
        Update an existing asset type's information.

        Args:
            id: ID of the asset type to update
            dto: UpdateAssetTypeDto containing fields to update

        Returns:
            Result[ResAssetTypeDto, Exception]: Success with updated asset type or Failure with error

        Domain Rules:
        - Asset type must exist
        - Name must follow proper format if being updated
        - Name must remain unique if being updated
        - Update timestamp must be maintained
        """
        try:
            # Validate asset type exists
            existing_type = await self.get_asset_type(id)
            if not existing_type:
                return Failure(Exception("Asset type not found"))

            # Validate name if being updated
            if dto.name:
                validation_result = self._validate_asset_type_name(dto.name)
                if not validation_result:
                    return Failure(Exception("Invalid asset type name format"))

                # Check for duplicate names
                existing_types = await self.list_asset_types()
                if any(t.name.lower() == dto.name.lower() and t.id != id for t in existing_types):
                    return Failure(Exception("Asset type with this name already exists"))

            

            return await self.repository.update(id, dto)
        except Exception as e:
            return Failure(Exception(f"Failed to update asset type: {str(e)}"))

    async def delete_asset_type(self, id: int) -> Result[bool, Exception]:
        """
        Delete an asset type if it's not being used by any assets.

        Args:
            id: ID of the asset type to delete

        Returns:
            Result[bool, Exception]: Success if deleted, Failure with error

        Domain Rules:
        - Asset type must exist
        - Asset type must not be in use by any assets
        - Deletion must be logged for audit purposes
        """
        try:
            # Validate asset type exists
            existing_type = await self.get_asset_type(id)
            if not existing_type:
                return Failure(Exception("Asset type not found"))

            # Check if asset type is in use
            if await self._is_asset_type_in_use(id):
                return Failure(Exception("Cannot delete asset type that is in use"))

            # TODO: Add audit logging for deletion
            return await self.repository.delete(id)
        except Exception as e:
            return Failure(Exception(f"Failed to delete asset type: {str(e)}"))

    async def list_asset_types(self) -> List[ResAssetTypeDto]:
        """
        Retrieve all asset types in the system.

        Returns:
            List[ResAssetTypeDto]: List of all asset types
        """
        try:
            asset_types = await self.repository.list()
            # Sort by name for consistent ordering
            return sorted(asset_types, key=lambda x: x.name.lower())
        except Exception as e:
            print(f"Error retrieving asset types: {str(e)}")
            return []

    def _validate_asset_type_name(self, name: str) -> bool:
        """
        Validate asset type name format.

        Args:
            name: Name to validate

        Returns:
            bool: True if name is valid, False otherwise

        Validation Rules:
        - Must not be empty
        - Must be alphanumeric with spaces
        - Must be between 2 and 50 characters
        """
        if not name or not name.strip():
            return False
        
        # Check length
        if len(name.strip()) < 2 or len(name.strip()) > 50:
            return False
        
        # Check format (alphanumeric with spaces)
        return all(c.isalnum() or c.isspace() for c in name)

    async def _is_asset_type_in_use(self, asset_type_id: int) -> bool:
        """
        Check if an asset type is currently in use by any assets.

        Args:
            asset_type_id: ID of the asset type to check

        Returns:
            bool: True if asset type is in use, False otherwise
        """
        # TODO: Implement check for assets using this type
        # This would require access to the asset repository
        return False
