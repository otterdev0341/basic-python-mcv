from ...server import MCPServer
from ...application.usecase.expense_type_usecase import ExpenseTypeUseCase
from domain.value_objects.dto import CreateExpenseTypeDto, UpdateExpenseTypeDto, ResExpenseTypeDto
from returns.result import Result
from typing import Optional, List

"""
Expense Type Resources Documentation
==================================

English:
This module manages expense categories/types in the system.
It provides endpoints for creating, reading, updating, and deleting expense types.

Key Features:
- Create new expense categories
- Retrieve expense type information
- Update expense type details
- Delete expense types when appropriate
- List all available expense types

Thai:
โมดูลนี้จัดการหมวดหมู่/ประเภทค่าใช้จ่ายในระบบ
ให้บริการ endpoints สำหรับการสร้าง อ่าน อัปเดต และลบประเภทค่าใช้จ่าย

คุณสมบัติหลัก:
- สร้างหมวดหมู่ค่าใช้จ่ายใหม่
- ดึงข้อมูลประเภทค่าใช้จ่าย
- อัปเดตรายละเอียดประเภทค่าใช้จ่าย
- ลบประเภทค่าใช้จ่ายเมื่อเหมาะสม
- แสดงรายการประเภทค่าใช้จ่ายทั้งหมดที่มี

DTOs Used:
----------
CreateExpenseTypeDto:
{
    name: str           # Name of the expense type/category
}

UpdateExpenseTypeDto:
{
    name?: str          # Optional new name for the expense type
}

ResExpenseTypeDto:
{
    id: int            # Unique identifier
    name: str          # Expense type name
    created_at: datetime # Creation timestamp
    updated_at: datetime # Last update timestamp
}
"""

def register_expense_type_resources(mcp: MCPServer, usecase: ExpenseTypeUseCase):
    @mcp.resource("expense-type://create")
    async def create(dto: CreateExpenseTypeDto) -> Result[ResExpenseTypeDto, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Create a new expense type.
        
        English:
        Creates a new expense category/type.
        Returns the created expense type details.
        
        Thai:
        สร้างหมวดหมู่/ประเภทค่าใช้จ่ายใหม่
        ส่งคืนรายละเอียดประเภทค่าใช้จ่ายที่สร้าง
        
        Args:
            dto (CreateExpenseTypeDto): Expense type creation details
            
        Returns:
            Result[ResExpenseTypeDto, Exception]: Created expense type details or error
        """
        return await usecase.create_expense_type(dto)

    @mcp.resource("expense-type://{id}")
    async def get(id: int) -> Optional[ResExpenseTypeDto]:  # type: ignore[reportUnusedFunction]
        """
        Get expense type by ID.
        
        English:
        Retrieves detailed information about a specific expense type.
        
        Thai:
        ดึงข้อมูลรายละเอียดของประเภทค่าใช้จ่ายที่ระบุ
        
        Args:
            id (int): Expense type ID
            
        Returns:
            Optional[ResExpenseTypeDto]: Expense type details if found, None otherwise
        """
        return await usecase.get_expense_type(id)

    @mcp.resource("expense-type://list")
    async def list_all() -> List[ResExpenseTypeDto]:  # type: ignore[reportUnusedFunction]
        """
        List all expense types.
        
        English:
        Retrieves a list of all expense types in the system.
        
        Thai:
        ดึงรายการประเภทค่าใช้จ่ายทั้งหมดในระบบ
        
        Returns:
            List[ResExpenseTypeDto]: List of all expense types
        """
        return await usecase.list_expense_types()

    @mcp.resource("expense-type://{id}/delete")
    async def delete(id: int) -> Result[bool, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Delete an expense type.
        
        English:
        Deletes an expense type if it has no linked expenses.
        
        Thai:
        ลบประเภทค่าใช้จ่ายหากไม่มีค่าใช้จ่ายที่เชื่อมโยง
        
        Args:
            id (int): Expense type ID to delete
            
        Returns:
            Result[bool, Exception]: Success if deleted, Failure with error message if failed
        """
        return await usecase.delete_expense_type(id)

    @mcp.resource("expense-type://{id}")
    async def update(id: int, dto: UpdateExpenseTypeDto) -> Result[ResExpenseTypeDto, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Update an expense type.
        
        English:
        Updates the details of an existing expense type.
        
        Thai:
        อัปเดตรายละเอียดของประเภทค่าใช้จ่ายที่มีอยู่
        
        Args:
            id (int): Expense type ID to update
            dto (UpdateExpenseTypeDto): New expense type details
            
        Returns:
            Result[ResExpenseTypeDto, Exception]: Updated expense type details or error
        """
        return await usecase.update_expense_type(id, dto) 