from typing import Optional, List
from returns.result import Result, Success, Failure

from datetime import datetime

from ...domain.value_objects.dto import (
    CreateTransactionDto,
    UpdateTransactionDto,
    ResTransactionDto,
    TransferFundDto,
    TransactionTypeEnum
)
from ...domain.repository.i_repository import CrudProtocol


class TransactionUseCase:
    def __init__(
        self,
        repository: CrudProtocol[
            CreateTransactionDto,
            UpdateTransactionDto,
            ResTransactionDto,
        ]
    ):
        self.repository = repository

    async def record_income(
        self, dto: CreateTransactionDto
    ) -> Result[ResTransactionDto, Exception]:
        """Record an income transaction."""
        if dto.transaction_type != TransactionTypeEnum.INCOME:
            return Failure(Exception("Transaction type must be Income"))
        return await self.repository.create(dto)

    async def record_payment(
        self, dto: CreateTransactionDto
    ) -> Result[ResTransactionDto, Exception]:
        """Record a payment transaction."""
        if dto.transaction_type != TransactionTypeEnum.PAYMENT:
            return Failure(Exception("Transaction type must be Payment"))
        if not dto.expense_id:
            return Failure(Exception("Payment must have an expense_id"))
        return await self.repository.create(dto)

    async def get_transaction(self, id: int) -> Optional[ResTransactionDto]:
        """Get a single transaction by ID."""
        return await self.repository.get(id)

    async def update_transaction(
        self, id: int, dto: UpdateTransactionDto
    ) -> Result[ResTransactionDto, Exception]:
        """Update an existing transaction."""
        return await self.repository.update(id, dto)

    async def delete_transaction(self, id: int) -> Result[bool, Exception]:
        """Delete a transaction if it's safe to do so."""
        return await self.repository.delete(id)

    async def list_transactions(self) -> List[ResTransactionDto]:
        """Get all transactions (both income and payments)."""
        return await self.repository.list()

    async def get_income_transactions(self) -> List[ResTransactionDto]:
        """Get only income transactions."""
        all_transactions = await self.repository.list()
        return [
            t for t in all_transactions 
            if t.transaction_type == TransactionTypeEnum.INCOME
        ]

    async def get_payment_transactions(self) -> List[ResTransactionDto]:
        """Get only payment transactions."""
        all_transactions = await self.repository.list()
        return [
            t for t in all_transactions 
            if t.transaction_type == TransactionTypeEnum.PAYMENT
        ]

    async def get_transactions_by_month(self, month: str) -> List[ResTransactionDto]:
        """Get all transactions in a given month (format: 'YYYY-MM')."""
        try:
            # Validate month format
            datetime.strptime(month, '%Y-%m')
            all_transactions = await self.repository.list()
            return [
                t for t in all_transactions 
                if t.created_at and t.created_at.strftime('%Y-%m') == month
            ]
        except ValueError:
            raise ValueError("Month must be in format 'YYYY-MM'")

    async def transfer_fund(self, dto: TransferFundDto) -> Result[bool, Exception]:
        """Transfer funds between assets."""
        # Create two transactions: one for withdrawal and one for deposit
        withdrawal_dto = CreateTransactionDto(
            transaction_type=TransactionTypeEnum.PAYMENT,
            amount=dto.amount,
            asset_id=dto.source_asset_id,
            note=f"Transfer to asset {dto.destination_asset_id}: {dto.note or ''}"
        )
        
        deposit_dto = CreateTransactionDto(
            transaction_type=TransactionTypeEnum.INCOME,
            amount=dto.amount,
            asset_id=dto.destination_asset_id,
            note=f"Transfer from asset {dto.source_asset_id}: {dto.note or ''}"
        )

        # Execute both transactions
        withdrawal_result = await self.record_payment(withdrawal_dto)
        if isinstance(withdrawal_result, Failure):
            return withdrawal_result

        deposit_result = await self.record_income(deposit_dto)
        if isinstance(deposit_result, Failure):
            # TODO: Implement rollback mechanism for the withdrawal
            return deposit_result

        return Success(True)
