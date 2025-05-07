from typing import List, Optional
from returns.result import Result, Failure
from ...domain.value_objects.dto import (
    CreateContactDto,
    UpdateContactDto,
    ResContactDto,
    ResContactTypeDto
)
from ...domain.repository.i_repository import CrudProtocol
from ...domain.entities.schema import ContactType


class ContactUseCase:
    """
    Contact Use Case implementation following Domain Driven Design principles.
    Handles all contact-related business operations including customers and vendors.
    """

    def __init__(self, repository: CrudProtocol[CreateContactDto, UpdateContactDto, ResContactDto]):
        self.repository = repository

    async def create_contact(
        self, dto: CreateContactDto
    ) -> Result[ResContactDto, Exception]:
        """
        Creates a new contact in the system.
        
        Args:
            dto: CreateContactDto containing contact details
                - name: Contact's name
                - business_name: Business name
                - phone: Contact phone number
                - description: Optional description
                - contact_type_id: Type of contact (customer/vendor)
        
        Returns:
            Result containing either the created contact or an error
        """
        return await self.repository.create(dto)

    async def create_customer(
        self, dto: CreateContactDto
    ) -> Result[ResContactDto, Exception]:
        """
        Creates a new customer contact.
        This is a convenience method that ensures the contact is created as a customer.
        
        Args:
            dto: CreateContactDto with customer details
        
        Returns:
            Result containing either the created customer or an error
        """
        # Ensure contact_type_id is set to customer type
        if not hasattr(dto, 'contact_type_id') or dto.contact_type_id != ContactType.CUSTOMER:
            return Failure(Exception("Contact type must be set to CUSTOMER"))
        return await self.repository.create(dto)

    async def create_vendor(
        self, dto: CreateContactDto
    ) -> Result[ResContactDto, Exception]:
        """
        Creates a new vendor contact.
        This is a convenience method that ensures the contact is created as a vendor.
        
        Args:
            dto: CreateContactDto with vendor details
        
        Returns:
            Result containing either the created vendor or an error
        """
        # Ensure contact_type_id is set to vendor type
        if not hasattr(dto, 'contact_type_id') or dto.contact_type_id != ContactType.VENDOR:
            return Failure(Exception("Contact type must be set to VENDOR"))
        return await self.repository.create(dto)

    async def get_all_contacts(self) -> List[ResContactDto]:
        """
        Retrieves all contacts from the system.
        
        Returns:
            List of all contacts with their details
        """
        return await self.repository.list()

    async def get_contact(self, id: int) -> Optional[ResContactDto]:
        """
        Retrieves a specific contact by ID.
        
        Args:
            id: The unique identifier of the contact
        
        Returns:
            Optional contact details if found, None otherwise
        """
        return await self.repository.get(id)

    async def update_contact(
        self, id: int, dto: UpdateContactDto
    ) -> Result[ResContactDto, Exception]:
        """
        Updates an existing contact's information.
        
        Args:
            id: The unique identifier of the contact to update
            dto: UpdateContactDto containing the fields to update
                - name: Optional new name
                - business_name: Optional new business name
                - phone: Optional new phone number
                - description: Optional new description
                - contact_type_id: Optional new contact type
        
        Returns:
            Result containing either the updated contact or an error
        """
        return await self.repository.update(id, dto)

    async def delete_contact(self, id: int) -> Result[bool, Exception]:
        """
        Deletes or deactivates a contact from the system.
        This operation is safe and will check for any dependencies before deletion.
        
        Args:
            id: The unique identifier of the contact to delete
        
        Returns:
            Result containing either True if successful or an error
        """
        return await self.repository.delete(id)

    async def get_customer_types(self) -> List[ResContactTypeDto]:
        """
        Retrieves all available contact types (e.g., Customer, Vendor).
        
        Returns:
            List of contact types with their details
        """
        # This would typically call a repository method to get contact types
        # For now, returning a placeholder implementation
        return []
