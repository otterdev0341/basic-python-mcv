from dataclasses import dataclass, field
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
)
from sqlalchemy.engine import URL
from src.config.db_config import DbConfig
@dataclass
class MysqlConnection:
    config: DbConfig

    engine: AsyncEngine = field(init=False)
    session_maker: async_sessionmaker[AsyncSession] = field(init=False)

    def __post_init__(self):
        # Create the URL for the SQLAlchemy engine
        url = URL.create(
            drivername="mysql+aiomysql",
            username=self.config.user,
            password=self.config.password,
            host=self.config.host,
            port=self.config.port,
            database=self.config.database
        )

        # Create the async engine
        self.engine = create_async_engine(url, echo=True, future=True)
        self.session_maker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )

    async def get_session(self) -> AsyncSession:
        return self.session_maker()

    async def get_connection(self):
        async with self.engine.connect() as conn:
            yield conn

    async def dispose(self):
        await self.engine.dispose()
