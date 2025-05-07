from ...server import MCPServer
from ...application.usecase.expense_usecase import ExpenseUseCase
from domain.value_objects.dto import CreateExpenseDto, UpdateExpenseDto, ResExpenseDto
from returns.result import Result
from typing import Optional, List

"""
Expense Resources Documentation
=============================

English:
This module manages expense categories and items in the system.
It provides endpoints for creating, reading, updating, and deleting expenses.

Key Features:
- Create new expense items
- Categorize expenses by type
- Update expense details
- Delete expenses when appropriate
- List all available expenses

Thai:
โมดูลนี้จัดการหมวดหมู่และรายการค่าใช้จ่ายในระบบ
ให้บริการ endpoints สำหรับการสร้าง อ่าน อัปเดต และลบค่าใช้จ่าย

คุณสมบัติหลัก:
- สร้างรายการค่าใช้จ่ายใหม่
- จัดหมวดหมู่ค่าใช้จ่ายตามประเภท
- อัปเดตรายละเอียดค่าใช้จ่าย
- ลบค่าใช้จ่ายเมื่อเหมาะสม
- แสดงรายการค่าใช้จ่ายทั้งหมดที่มี

DTOs Used:
----------
CreateExpenseDto:
{
    description: str        # Description of the expense
    expense_type_id: int   # ID of the expense type/category
}

UpdateExpenseDto:
{
    description?: str      # Optional new description
    expense_type_id?: int # Optional new expense type ID
}

ResExpenseDto:
{
    id: int               # Unique identifier
    description: str      # Expense description
    expense_type_id: int  # Expense type ID
    created_at: datetime  # Creation timestamp
    updated_at: datetime  # Last update timestamp
}
"""

def register_expense_resources(mcp: MCPServer, usecase: ExpenseUseCase):
    @mcp.resource("expense://create")
    async def create(dto: CreateExpenseDto) -> Result[ResExpenseDto, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Create a new expense.
        
        English:
        Creates a new expense item with description and type.
        Returns the created expense details.
        
        Thai:
        สร้างรายการค่าใช้จ่ายใหม่พร้อมคำอธิบายและประเภท
        ส่งคืนรายละเอียดค่าใช้จ่ายที่สร้าง
        
        Args:
            dto (CreateExpenseDto): Expense creation details
            
        Returns:
            Result[ResExpenseDto, Exception]: Created expense details or error
        """
        return await usecase.create_expense(dto)

    @mcp.resource("expense://{id}")
    async def get(id: int) -> Optional[ResExpenseDto]:  # type: ignore[reportUnusedFunction]
        """
        Get expense by ID.
        
        English:
        Retrieves detailed information about a specific expense.
        
        Thai:
        ดึงข้อมูลรายละเอียดของค่าใช้จ่ายที่ระบุ
        
        Args:
            id (int): Expense ID
            
        Returns:
            Optional[ResExpenseDto]: Expense details if found, None otherwise
        """
        return await usecase.get_expense(id)

    @mcp.resource("expense://list")
    async def list_all() -> List[ResExpenseDto]:  # type: ignore[reportUnusedFunction]
        """
        List all expenses.
        
        English:
        Retrieves a list of all expenses in the system.
        
        Thai:
        ดึงรายการค่าใช้จ่ายทั้งหมดในระบบ
        
        Returns:
            List[ResExpenseDto]: List of all expenses
        """
        return await usecase.list_expenses()

    @mcp.resource("expense://{id}/delete")
    async def delete(id: int) -> Result[bool, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Delete an expense.
        
        English:
        Deletes an expense if it has no linked transactions.
        
        Thai:
        ลบค่าใช้จ่ายหากไม่มีธุรกรรมที่เชื่อมโยง
        
        Args:
            id (int): Expense ID to delete
            
        Returns:
            Result[bool, Exception]: Success if deleted, Failure with error message if failed
        """
        return await usecase.delete_expense(id)

    @mcp.resource("expense://{id}")
    async def update(id: int, dto: UpdateExpenseDto) -> Result[ResExpenseDto, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Update an expense.
        
        English:
        Updates the details of an existing expense.
        
        Thai:
        อัปเดตรายละเอียดของค่าใช้จ่ายที่มีอยู่
        
        Args:
            id (int): Expense ID to update
            dto (UpdateExpenseDto): New expense details
            
        Returns:
            Result[ResExpenseDto, Exception]: Updated expense details or error
        """
        return await usecase.update_expense(id, dto) 