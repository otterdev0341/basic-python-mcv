from returns.result import Result
from ...domain.repository.i_tranfer_repository import TranferRepositoryProtocol
from ...domain.value_objects.dto import TransferFundDto


class TransferUseCase:
    def __init__(self, repo: TranferRepositoryProtocol) -> None:
        self._repo = repo

    async def execute(self, dto: TransferFundDto) -> Result[bool, Exception]:
        return await self._repo.transfer_fund(dto)