from typing import Optional, List
from returns.result import Result, Failure


from ...domain.value_objects.dto import (
    CreateExpenseTypeDto,
    UpdateExpenseTypeDto,
    ResExpenseTypeDto,
)
from ...domain.repository.i_repository import CrudProtocol



class ExpenseTypeUseCase:
    """
    Use case for managing expense types in the system.
    This class handles all business logic related to expense type operations.
    """

    def __init__(self, repository: CrudProtocol[CreateExpenseTypeDto, UpdateExpenseTypeDto, ResExpenseTypeDto]):
        """
        Initialize the expense type use case with its repository.

        Args:
            repository: Repository implementing the CrudProtocol for expense types
        """
        self.repository = repository

    async def create_expense_type(
        self, dto: CreateExpenseTypeDto
    ) -> Result[ResExpenseTypeDto, Exception]:
        """
        Create a new expense type in the system.

        Args:
            dto: Data transfer object containing expense type creation details
                { name: str }

        Returns:
            Result containing either the created expense type or an exception
        """
        try:
            # Validate expense type name
            if not dto.name or len(dto.name.strip()) == 0:
                return Failure(Exception("Expense type name cannot be empty"))

            return await self.repository.create(dto)
        except Exception as e:
            return Failure(e)

    async def get_expense_type(self, id: int) -> Optional[ResExpenseTypeDto]:
        """
        Retrieve a specific expense type by its ID.

        Args:
            id: The unique identifier of the expense type

        Returns:
            Optional expense type DTO if found, None otherwise
        """
        return await self.repository.get(id)

    async def update_expense_type(
        self, id: int, dto: UpdateExpenseTypeDto
    ) -> Result[ResExpenseTypeDto, Exception]:
        """
        Update an existing expense type.

        Args:
            id: The unique identifier of the expense type to update
            dto: Data transfer object containing update details
                { name?: str }

        Returns:
            Result containing either the updated expense type or an exception
        """
        try:
            # Check if expense type exists
            existing_type = await self.repository.get(id)
            if not existing_type:
                return Failure(Exception("Expense type not found"))

            # Validate update data
            if dto.name and len(dto.name.strip()) == 0:
                return Failure(Exception("Expense type name cannot be empty"))

            return await self.repository.update(id, dto)
        except Exception as e:
            return Failure(e)

    async def delete_expense_type(self, id: int) -> Result[bool, Exception]:
        """
        Delete an expense type if it's not being used by any expenses.

        Args:
            id: The unique identifier of the expense type to delete

        Returns:
            Result containing either True if deleted successfully or an exception
        """
        try:
            # Check if expense type exists
            existing_type = await self.repository.get(id)
            if not existing_type:
                return Failure(Exception("Expense type not found"))

            # TODO: Add check for linked expenses before deletion
            # This would require additional repository method to check for linked expenses

            return await self.repository.delete(id)
        except Exception as e:
            return Failure(e)

    async def list_expense_types(self) -> List[ResExpenseTypeDto]:
        """
        Retrieve all expense types in the system.

        Returns:
            List of expense type DTOs
        """
        return await self.repository.list()

    async def get_expense_type_by_name(self, name: str) -> Optional[ResExpenseTypeDto]:
        """
        Find an expense type by its name.

        Args:
            name: The name of the expense type to find

        Returns:
            Optional expense type DTO if found, None otherwise
        """
        # This would require additional repository method to search by name
        # Implementation depends on repository capabilities
        raise NotImplementedError("Search by name not implemented in repository")
