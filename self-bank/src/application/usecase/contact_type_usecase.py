from typing import List, Optional
from returns.result import Result, Success, Failure

from ...domain.value_objects.dto import (
    CreateContactTypeDto,
    UpdateContactTypeDto,
    ResContactTypeDto,
)
from ...domain.repository.i_repository import CrudProtocol


class ContactTypeUseCase:
    """
    Use case for managing contact types (e.g., Customer, Vendor) in the system.
    This class handles all business logic related to contact type operations.
    """
    def __init__(self, repository: CrudProtocol[CreateContactTypeDto, UpdateContactTypeDto, ResContactTypeDto]):
        self.repository = repository

    async def create_contact_type(
        self, dto: CreateContactTypeDto
    ) -> Result[ResContactTypeDto, Exception]:
        """
        Creates a new contact type in the system.
        
        Args:
            dto: CreateContactTypeDto containing the contact type details
            
        Returns:
            Result containing either the created contact type or an error
        """
        return await self.repository.create(dto)

    async def get_contact_type(self, id: int) -> Optional[ResContactTypeDto]:
        """
        Retrieves a specific contact type by its ID.
        
        Args:
            id: The unique identifier of the contact type
            
        Returns:
            Optional[ResContactTypeDto]: The contact type if found, None otherwise
        """
        return await self.repository.get(id)

    async def update_contact_type(
        self, id: int, dto: UpdateContactTypeDto
    ) -> Result[ResContactTypeDto, Exception]:
        """
        Updates an existing contact type with new information.
        
        Args:
            id: The unique identifier of the contact type to update
            dto: UpdateContactTypeDto containing the new contact type details
            
        Returns:
            Result containing either the updated contact type or an error
        """
        return await self.repository.update(id, dto)

    async def delete_contact_type(self, id: int) -> Result[bool, Exception]:
        """
        Deletes a contact type from the system.
        Note: This operation should be used with caution as it may affect existing contacts.
        
        Args:
            id: The unique identifier of the contact type to delete
            
        Returns:
            Result containing either True if deletion was successful or an error
        """
        return await self.repository.delete(id)

    async def list_contact_types(self) -> List[ResContactTypeDto]:
        """
        Retrieves all contact types in the system.
        
        Returns:
            List[ResContactTypeDto]: A list of all contact types
        """
        return await self.repository.list()

    async def get_customer_type(self) -> Optional[ResContactTypeDto]:
        """
        Retrieves the specific contact type for customers.
        This is a convenience method for common operations.
        
        Returns:
            Optional[ResContactTypeDto]: The customer contact type if found, None otherwise
        """
        types = await self.list_contact_types()
        return next((t for t in types if t.name.lower() == "customer"), None)

    async def get_vendor_type(self) -> Optional[ResContactTypeDto]:
        """
        Retrieves the specific contact type for vendors.
        This is a convenience method for common operations.
        
        Returns:
            Optional[ResContactTypeDto]: The vendor contact type if found, None otherwise
        """
        types = await self.list_contact_types()
        return next((t for t in types if t.name.lower() == "vendor"), None)
