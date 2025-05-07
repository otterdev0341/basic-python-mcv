from ...server import MCPServer
from ...application.usecase.assest_usecase import AssetUseCase
from domain.value_objects.dto import CreateAssetDto, UpdateAssetDto, ResAssetDto
from returns.result import Result
from typing import Optional, List

"""
Asset Resources Documentation
===========================

English:
This module manages assets in the system (e.g., bank accounts, wallets, etc.).
It provides endpoints for creating, reading, updating, and deleting assets.

Key Features:
- Create new assets with specific types
- Retrieve asset information
- Update asset details
- Delete assets when appropriate
- List all available assets

Thai:
โมดูลนี้จัดการสินทรัพย์ในระบบ (เช่น บัญชีธนาคาร กระเป๋าเงิน ฯลฯ)
ให้บริการ endpoints สำหรับการสร้าง อ่าน อัปเดต และลบสินทรัพย์

คุณสมบัติหลัก:
- สร้างสินทรัพย์ใหม่พร้อมระบุประเภท
- ดึงข้อมูลสินทรัพย์
- อัปเดตรายละเอียดสินทรัพย์
- ลบสินทรัพย์เมื่อเหมาะสม
- แสดงรายการสินทรัพย์ทั้งหมดที่มี

DTOs Used:
----------
CreateAssetDto:
{
    name: str           # Name of the asset
    asset_type_id: int  # ID of the asset type
}

UpdateAssetDto:
{
    name?: str          # Optional new name for the asset
    asset_type_id?: int # Optional new asset type ID
}

ResAssetDto:
{
    id: int            # Unique identifier
    name: str          # Asset name
    asset_type_id: int # Asset type ID
    created_at: datetime # Creation timestamp
    updated_at: datetime # Last update timestamp
}
"""

def register_asset_resources(mcp: MCPServer, usecase: AssetUseCase):
    @mcp.resource("asset://create")
    async def create(dto: CreateAssetDto) -> Result[ResAssetDto, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Create a new asset.
        
        English:
        Creates a new asset with the specified name and type.
        Returns the created asset details.
        
        Thai:
        สร้างสินทรัพย์ใหม่พร้อมระบุชื่อและประเภท
        ส่งคืนรายละเอียดสินทรัพย์ที่สร้าง
        
        Args:
            dto (CreateAssetDto): Asset creation details
            
        Returns:
            Result[ResAssetDto, Exception]: Created asset details or error
        """
        return await usecase.create_asset(dto)

    @mcp.resource("asset://{id}")
    async def get(id: int) -> Optional[ResAssetDto]:  # type: ignore[reportUnusedFunction]
        """
        Get asset by ID.
        
        English:
        Retrieves detailed information about a specific asset.
        
        Thai:
        ดึงข้อมูลรายละเอียดของสินทรัพย์ที่ระบุ
        
        Args:
            id (int): Asset ID
            
        Returns:
            Optional[ResAssetDto]: Asset details if found, None otherwise
        """
        return await usecase.get_asset(id)

    @mcp.resource("asset://list")
    async def list_all() -> List[ResAssetDto]:  # type: ignore[reportUnusedFunction]
        """
        List all assets.
        
        English:
        Retrieves a list of all assets in the system.
        
        Thai:
        ดึงรายการสินทรัพย์ทั้งหมดในระบบ
        
        Returns:
            List[ResAssetDto]: List of all assets
        """
        return await usecase.get_all_assets()

    @mcp.resource("asset://{id}/delete")
    async def delete(id: int) -> Result[bool, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Delete an asset.
        
        English:
        Deletes an asset if it has no linked transactions.
        
        Thai:
        ลบสินทรัพย์หากไม่มีธุรกรรมที่เชื่อมโยง
        
        Args:
            id (int): Asset ID to delete
            
        Returns:
            Result[bool, Exception]: Success if deleted, Failure with error message if failed
        """
        return await usecase.delete_asset(id)

    @mcp.resource("asset://{id}")
    async def update(id: int, dto: UpdateAssetDto) -> Result[ResAssetDto, Exception]:  # type: ignore[reportUnusedFunction]
        """
        Update an asset.
        
        English:
        Updates the details of an existing asset.
        
        Thai:
        อัปเดตรายละเอียดของสินทรัพย์ที่มีอยู่
        
        Args:
            id (int): Asset ID to update
            dto (UpdateAssetDto): New asset details
            
        Returns:
            Result[ResAssetDto, Exception]: Updated asset details or error
        """
        return await usecase.update_asset(id, dto) 