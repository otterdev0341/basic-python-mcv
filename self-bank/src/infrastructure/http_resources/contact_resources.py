from ...server import MCPServer
from ...application.usecase.contact_usecase import ContactUseCase
from domain.value_objects.dto import CreateContactDto, ResContactDto, UpdateContactDto
from returns.result import Result
from typing import Optional, List

"""
Contact Resources Documentation
=============================

English:
This module manages contacts in the system (customers, vendors, etc.).
It provides endpoints for creating, reading, updating, and deleting contacts.

Key Features:
- Create new contacts with business details
- Retrieve contact information
- Update contact details
- Delete contacts when appropriate
- List all available contacts

Thai:
โมดูลนี้จัดการรายชื่อผู้ติดต่อในระบบ (ลูกค้า ผู้จำหน่าย ฯลฯ)
ให้บริการ endpoints สำหรับการสร้าง อ่าน อัปเดต และลบผู้ติดต่อ

คุณสมบัติหลัก:
- สร้างผู้ติดต่อใหม่พร้อมรายละเอียดทางธุรกิจ
- ดึงข้อมูลผู้ติดต่อ
- อัปเดตรายละเอียดผู้ติดต่อ
- ลบผู้ติดต่อเมื่อเหมาะสม
- แสดงรายการผู้ติดต่อทั้งหมดที่มี

DTOs Used:
----------
CreateContactDto:
{
    name: str           # Full name of the contact
    business_name: str  # Name of the business/organization
    phone: str         # Contact phone number
    description?: str  # Optional additional information
    contact_type_id: int # ID of the contact type (customer/vendor)
}

UpdateContactDto:
{
    name?: str          # Optional new name
    business_name?: str # Optional new business name
    phone?: str        # Optional new phone number
    description?: str  # Optional new description
    contact_type_id?: int # Optional new contact type
}

ResContactDto:
{
    id: int            # Unique identifier
    name: str          # Contact name
    business_name: str # Business name
    phone: str        # Phone number
    description?: str  # Additional information
    contact_type_id: int # Contact type ID
    created_at: datetime # Creation timestamp
    updated_at: datetime # Last update timestamp
}
"""

def register_contact_resources(mcp: MCPServer, usecase: ContactUseCase):
    @mcp.resource("contact://create")
    async def create(dto: CreateContactDto) -> Result[ResContactDto, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Create a new contact.
        
        English:
        Creates a new contact with business details and type.
        Returns the created contact information.
        
        Thai:
        สร้างผู้ติดต่อใหม่พร้อมรายละเอียดทางธุรกิจและประเภท
        ส่งคืนข้อมูลผู้ติดต่อที่สร้าง
        
        Args:
            dto (CreateContactDto): Contact creation details including name, business, and type
            
        Returns:
            Result[ResContactDto, Exception]: Created contact details or error
        """
        return await usecase.create_contact(dto)

    @mcp.resource("contact://{id}")
    async def get(id: int) -> Optional[ResContactDto]:  # type: ignore[reportUnusedFunction]
        """
        Get contact by ID.
        
        English:
        Retrieves detailed information about a specific contact.
        
        Thai:
        ดึงข้อมูลรายละเอียดของผู้ติดต่อที่ระบุ
        
        Args:
            id (int): Contact ID
            
        Returns:
            Optional[ResContactDto]: Contact details if found, None otherwise
        """
        return await usecase.get_contact(id)

    @mcp.resource("contact://list")
    async def list_all() -> List[ResContactDto]:  # type: ignore[reportUnusedFunction]
        """
        List all contacts.
        
        English:
        Retrieves a list of all contacts in the system.
        
        Thai:
        ดึงรายการผู้ติดต่อทั้งหมดในระบบ
        
        Returns:
            List[ResContactDto]: List of all contacts
        """
        return await usecase.get_all_contacts()

    @mcp.resource("contact://{id}/delete")
    async def delete(id: int) -> Result[bool, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Delete a contact.
        
        English:
        Deletes a contact if it has no linked transactions.
        
        Thai:
        ลบผู้ติดต่อหากไม่มีธุรกรรมที่เชื่อมโยง
        
        Args:
            id (int): Contact ID to delete
            
        Returns:
            Result[bool, Exception]: Success if deleted, Failure with error message if failed
        """
        return await usecase.delete_contact(id)

    @mcp.resource("contact://{id}")
    async def update(id: int, dto: UpdateContactDto) -> Result[ResContactDto, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Update a contact.
        
        English:
        Updates the details of an existing contact.
        
        Thai:
        อัปเดตรายละเอียดของผู้ติดต่อที่มีอยู่
        
        Args:
            id (int): Contact ID to update
            dto (UpdateContactDto): New contact details
            
        Returns:
            Result[ResContactDto, Exception]: Updated contact details or error
        """
        return await usecase.update_contact(id, dto)