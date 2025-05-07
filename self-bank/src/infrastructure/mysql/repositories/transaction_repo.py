from ....domain.repository.i_repository import CrudProtocol
from typing import Optional, List
from returns.result import Result, Success, Failure
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from .base_repository import BaseRepository
from ....domain.entities.schema import Transaction
from ....domain.value_objects.dto import (
    CreateTransactionDto,
    UpdateTransactionDto,
    ResTransactionDto
)


class TransactionRepository(
    BaseRepository,
    CrudProtocol[CreateTransactionDto, UpdateTransactionDto, ResTransactionDto]
):
    async def create(self, dto: CreateTransactionDto) -> Result[ResTransactionDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                transaction = Transaction(
                    transaction_type=dto.transaction_type,
                    amount=dto.amount,
                    asset_id=dto.asset_id,
                    expense_id=dto.expense_id,
                    contact_id=dto.contact_id,
                    note=dto.note,
                )
                session.add(transaction)
                await session.commit()
                await session.refresh(transaction)
                return Success(ResTransactionDto.model_validate(transaction))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def get(self, id: int) -> Optional[ResTransactionDto]:
        async with await self._db.get_session() as session:
            result = await session.get(Transaction, id)
            if result:
                return ResTransactionDto.model_validate(result)
            return None

    async def update(self, id: int, dto: UpdateTransactionDto) -> Result[ResTransactionDto, Exception]:
        async with await self._db.get_session() as session:
            try:
                transaction = await session.get(Transaction, id)
                if not transaction:
                    return Failure(Exception("Transaction not found"))

                for field, value in dto.model_dump(exclude_unset=True).items():
                    setattr(transaction, field, value)

                await session.commit()
                await session.refresh(transaction)
                return Success(ResTransactionDto.model_validate(transaction))
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def delete(self, id: int) -> Result[bool, Exception]:
        async with await self._db.get_session() as session:
            try:
                transaction = await session.get(Transaction, id)
                if not transaction:
                    return Failure(Exception("Transaction not found"))

                await session.delete(transaction)
                await session.commit()
                return Success(True)
            except SQLAlchemyError as e:
                await session.rollback()
                return Failure(e)

    async def list(self) -> List[ResTransactionDto]:
        async with await self._db.get_session() as session:
            result = await session.execute(select(Transaction))
            records = result.scalars().all()
            return [ResTransactionDto.model_validate(r) for r in records]
