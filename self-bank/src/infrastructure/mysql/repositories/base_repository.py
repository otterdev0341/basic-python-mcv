from sqlalchemy.ext.asyncio import AsyncSession
from ...mysql.mysql_connection import MysqlConnection

class BaseRepository:
    def __init__(self, db: MysqlConnection):
        self._db = db

    async def get_session(self) -> AsyncSession:
        return await self._db.get_session()