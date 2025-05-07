from typing import Protocol
from returns.result import Result
from ...domain.value_objects.dto import TransferFundDto


class TranferRepositoryProtocol(Protocol):


    # 👇 Add this line to the protocol
    async def transfer_fund(self, dto: TransferFundDto) -> Result[bool, Exception]: ...
