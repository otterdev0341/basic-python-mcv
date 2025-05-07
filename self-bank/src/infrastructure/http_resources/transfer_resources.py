from ...server import MCPServer
from ...application.usecase.tranfer_usecase import TransferUseCase
from domain.value_objects.dto import TransferFundDto
from returns.result import Result


"""
Transfer Resources Documentation
==============================

English:
This module handles fund transfers between assets in the system.
It provides endpoints for transferring funds from one asset to another.

Key Features:
- Transfer funds between different assets
- Validate transfer amounts and asset existence
- Maintain transaction history

Thai:
โมดูลนี้จัดการการโอนเงินระหว่างสินทรัพย์ในระบบ
ให้บริการ endpoints สำหรับการโอนเงินจากสินทรัพย์หนึ่งไปยังอีกสินทรัพย์หนึ่ง

คุณสมบัติหลัก:
- โอนเงินระหว่างสินทรัพย์ที่แตกต่างกัน
- ตรวจสอบจำนวนเงินที่โอนและความมีอยู่ของสินทรัพย์
- บันทึกประวัติการทำธุรกรรม

DTOs Used:
----------
TransferFundDto:
{
    source_asset_id: int      # ID of the asset to transfer from
    destination_asset_id: int # ID of the asset to transfer to
    amount: Decimal          # Amount to transfer (must be positive)
    note: Optional[str]      # Optional note about the transfer
}
"""

def register_transfer_resources(mcp: MCPServer, usecase: TransferUseCase):
    @mcp.resource("transfer://fund")
    async def transfer_fund(dto: TransferFundDto) -> Result[bool, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Transfer funds between assets.
        
        English:
        This endpoint handles the transfer of funds between two assets.
        It validates the transfer amount and ensures sufficient funds are available.
        
        Thai:
        endpoint นี้จัดการการโอนเงินระหว่างสินทรัพย์สองรายการ
        ตรวจสอบจำนวนเงินที่โอนและตรวจสอบว่ามีเงินเพียงพอ
        
        Args:
            dto (TransferFundDto): Transfer details including source, destination, and amount
            
        Returns:
            Result[bool, Exception]: Success if transfer completed, Failure with error message if failed
        """
        return await usecase.transfer_fund(dto) 