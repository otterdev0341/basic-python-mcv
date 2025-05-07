from typing import Optional, List
from returns.result import Result, Failure


from ...domain.value_objects.dto import (
    CreateExpenseDto,
    UpdateExpenseDto,
    ResExpenseDto,
)
from ...domain.repository.i_repository import CrudProtocol


class ExpenseUseCase:
    """
    Expense Use Case - Handles all expense-related business operations
    following Domain Driven Design principles.
    
    This use case encapsulates the business logic for managing expenses,
    including creation, retrieval, updates, and deletion of expense records.
    """

    def __init__(self, repository: CrudProtocol[CreateExpenseDto, UpdateExpenseDto, ResExpenseDto]):
        """
        Initialize the Expense Use Case with its repository.
        
        Args:
            repository: Repository implementing the CrudProtocol for expense operations
        """
        self.repository = repository

    async def create_expense(
        self, dto: CreateExpenseDto
    ) -> Result[ResExpenseDto, Exception]:
        """
        Create a new expense item in the system.
        
        Args:
            dto: CreateExpenseDto containing description and expense_type_id
            
        Returns:
            Result containing either the created expense or an error
        """
        try:
            # Validate expense type exists
            if not dto.expense_type_id:
                return Failure(Exception("Expense type is required"))
            
            # Validate description is not empty
            if not dto.description or not dto.description.strip():
                return Failure(Exception("Expense description cannot be empty"))
            
            return await self.repository.create(dto)
        except Exception as e:
            return Failure(e)

    async def get_expense(self, id: int) -> Optional[ResExpenseDto]:
        """
        Retrieve a specific expense by its ID.
        
        Args:
            id: The unique identifier of the expense
            
        Returns:
            Optional[ResExpenseDto]: The expense if found, None otherwise
        """
        return await self.repository.get(id)

    async def update_expense(
        self, id: int, dto: UpdateExpenseDto
    ) -> Result[ResExpenseDto, Exception]:
        """
        Update an existing expense record.
        
        Args:
            id: The ID of the expense to update
            dto: UpdateExpenseDto containing the fields to update
            
        Returns:
            Result containing either the updated expense or an error
        """
        try:
            # Check if expense exists
            existing_expense = await self.get_expense(id)
            if not existing_expense:
                return Failure(Exception(f"Expense with ID {id} not found"))
            
            # Validate update data
            if dto.description and not dto.description.strip():
                return Failure(Exception("Expense description cannot be empty"))
            
            return await self.repository.update(id, dto)
        except Exception as e:
            return Failure(e)

    async def delete_expense(self, id: int) -> Result[bool, Exception]:
        """
        Delete an expense if it's safe to do so (no linked transactions).
        
        Args:
            id: The ID of the expense to delete
            
        Returns:
            Result containing either True if deleted or an error
        """
        try:
            # Check if expense exists
            existing_expense = await self.get_expense(id)
            if not existing_expense:
                return Failure(Exception(f"Expense with ID {id} not found"))
            
            # TODO: Add check for linked transactions before deletion
            # This would require additional repository methods
            
            return await self.repository.delete(id)
        except Exception as e:
            return Failure(e)

    async def list_expenses(self) -> List[ResExpenseDto]:
        """
        Retrieve all defined expense items in the system.
        
        Returns:
            List of all expense records
        """
        return await self.repository.list()
