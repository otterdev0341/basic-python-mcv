from returns.result import Result, Failure
from ...domain.repository.i_tranfer_repository import TranferRepositoryProtocol
from ...domain.value_objects.dto import TransferFundDto
from decimal import Decimal


class TransferUseCase:
    def __init__(self, repo: TranferRepositoryProtocol) -> None:
        self._repo = repo

    async def transfer_fund(self, dto: TransferFundDto) -> Result[bool, Exception]:
        """
        Transfer funds between assets.
        
        Args:
            dto (TransferFundDto): Transfer details including source, destination, and amount
            
        Returns:
            Result[bool, Exception]: Success if transfer completed, Failure with error message if failed
            
        Business Rules:
        1. Source and destination assets must be different
        2. Amount must be positive
        3. Source asset must have sufficient funds
        4. Both assets must exist
        """
        try:
            # Validate transfer amount
            if dto.amount <= Decimal('0'):
                return Failure(ValueError("Transfer amount must be greater than zero"))

            # Validate source and destination are different
            if dto.source_asset_id == dto.destination_asset_id:
                return Failure(ValueError("Source and destination assets must be different"))

            # Execute transfer through repository
            return await self._repo.transfer_fund(dto)

        except Exception as e:
            return Failure(e)