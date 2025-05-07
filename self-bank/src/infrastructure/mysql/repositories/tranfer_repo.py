from returns.result import Result, Success, Failure
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from .base_repository import BaseRepository
from ....domain.entities.schema import CurrentSheet, Transaction, TransactionType
from ....domain.repository.i_tranfer_repository import TranferRepositoryProtocol
from ....domain.value_objects.dto import TransferFundDto


class TransferRepository(BaseRepository, TranferRepositoryProtocol):
    async def transfer_fund(self, dto: TransferFundDto) -> Result[bool, Exception]:
        async with await self._db.get_session() as session:
            try:
                # Fetch source balance
                source_result = await session.execute(
                    select(CurrentSheet).where(CurrentSheet.asset_id == dto.source_asset_id)
                )
                source_sheet = source_result.scalar_one_or_none()

                # Fetch destination balance
                dest_result = await session.execute(
                    select(CurrentSheet).where(CurrentSheet.asset_id == dto.destination_asset_id)
                )
                dest_sheet = dest_result.scalar_one_or_none()

                if not source_sheet or not dest_sheet:
                    return Failure(Exception("Source or destination asset not found."))

                current_source_balance = float(source_sheet.balance.value)
                current_dest_balance = float(dest_sheet.balance.value)

                if current_source_balance < float(dto.amount):
                    return Failure(Exception("Insufficient funds in source asset."))

                # Create transaction
                txn = Transaction(
                    transaction_type=TransactionType.TRANSFER,
                    amount=dto.amount,
                    asset_id=dto.source_asset_id,
                    destination_asset_id=dto.destination_asset_id,
                    note=dto.note
                )
                session.add(txn)

                # Update balances using setattr
                setattr(source_sheet, 'balance', current_source_balance - float(dto.amount))
                setattr(dest_sheet, 'balance', current_dest_balance + float(dto.amount))

                await session.commit()
                return Success(True)
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)
