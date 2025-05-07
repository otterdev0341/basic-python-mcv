from ...server import MCPServer
from ...application.usecase.transaction_usecase import TransactionUseCase
from domain.value_objects.dto import CreateTransactionDto, ResTransactionDto
from returns.result import Result
from typing import List

"""
Transaction Resources Documentation
=================================

English:
This module manages financial transactions in the system.
It handles income, payments, and provides transaction history.

Key Features:
- Record income transactions
- Record payment transactions
- Retrieve transaction history
- Filter transactions by type and date
- Get monthly transaction summaries

Thai:
โมดูลนี้จัดการธุรกรรมทางการเงินในระบบ
จัดการรายรับ การชำระเงิน และให้ประวัติธุรกรรม

คุณสมบัติหลัก:
- บันทึกธุรกรรมรายรับ
- บันทึกธุรกรรมรายจ่าย
- ดึงประวัติธุรกรรม
- กรองธุรกรรมตามประเภทและวันที่
- ดูสรุปรายเดือนของธุรกรรม

DTOs Used:
----------
CreateTransactionDto:
{
    transaction_type: TransactionTypeEnum  # 'Income' or 'Payment'
    amount: Decimal                       # Transaction amount
    asset_id: int                         # ID of the affected asset
    expense_id?: int                      # Optional expense ID for payments
    contact_id?: int                      # Optional contact ID
    note?: str                           # Optional transaction note
}

ResTransactionDto:
{
    id: int                              # Transaction ID
    transaction_type: TransactionTypeEnum # Type of transaction
    amount: Decimal                      # Transaction amount
    asset_id: int                        # Affected asset ID
    expense_id?: int                     # Related expense ID if any
    contact_id?: int                     # Related contact ID if any
    note?: str                          # Transaction note
    created_at: datetime                 # Transaction timestamp
    updated_at: datetime                 # Last update timestamp
}
"""

def register_transaction_resources(mcp: MCPServer, usecase: TransactionUseCase):
    @mcp.resource("http://transaction/income")
    async def record_income(dto: CreateTransactionDto) -> Result[ResTransactionDto, Exception]:
        """
        Record an income transaction.
        
        English:
        Records a new income transaction in the system.
        
        Thai:
        บันทึกธุรกรรมรายรับใหม่ในระบบ
        
        Args:
            dto (CreateTransactionDto): Income transaction details
            
        Returns:
            Result[ResTransactionDto, Exception]: Recorded transaction or error
        """
        return await usecase.record_income(dto)

    @mcp.resource("http://transaction/payment")
    async def record_payment(dto: CreateTransactionDto) -> Result[ResTransactionDto, Exception]:
        """
        Record a payment transaction.
        
        English:
        Records a new payment transaction in the system.
        
        Thai:
        บันทึกธุรกรรมรายจ่ายใหม่ในระบบ
        
        Args:
            dto (CreateTransactionDto): Payment transaction details
            
        Returns:
            Result[ResTransactionDto, Exception]: Recorded transaction or error
        """
        return await usecase.record_payment(dto)

    @mcp.resource("http://transaction/list")
    async def list_all() -> List[ResTransactionDto]:
        """
        List all transactions.
        
        English:
        Retrieves all transactions in the system.
        
        Thai:
        ดึงธุรกรรมทั้งหมดในระบบ
        
        Returns:
            List[ResTransactionDto]: List of all transactions
        """
        return await usecase.list_transactions()

    @mcp.resource("http://transaction/income/list")
    async def list_income() -> List[ResTransactionDto]:
        """
        List income transactions.
        
        English:
        Retrieves all income transactions.
        
        Thai:
        ดึงธุรกรรมรายรับทั้งหมด
        
        Returns:
            List[ResTransactionDto]: List of income transactions
        """
        return await usecase.get_income_transactions()

    @mcp.resource("http://transaction/payment/list")
    async def list_payments() -> List[ResTransactionDto]:
        """
        List payment transactions.
        
        English:
        Retrieves all payment transactions.
        
        Thai:
        ดึงธุรกรรมรายจ่ายทั้งหมด
        
        Returns:
            List[ResTransactionDto]: List of payment transactions
        """
        return await usecase.get_payment_transactions()

    @mcp.resource("http://transaction/month/{month}")
    async def get_by_month(month: str) -> List[ResTransactionDto]:
        """
        Get transactions by month.
        
        English:
        Retrieves all transactions for a specific month.
        
        Thai:
        ดึงธุรกรรมทั้งหมดสำหรับเดือนที่ระบุ
        
        Args:
            month (str): Month in 'YYYY-MM' format
            
        Returns:
            List[ResTransactionDto]: List of transactions for the month
        """
        return await usecase.get_transactions_by_month(month) 