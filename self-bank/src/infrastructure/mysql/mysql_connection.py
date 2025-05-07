from dataclasses import dataclass, field
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
)
from sqlalchemy.engine import URL


@dataclass
class MysqlConnection:
    user: str
    password: str
    host: str
    port: int
    database: str

    engine: AsyncEngine = field(init=False)
    session_maker: async_sessionmaker[AsyncSession] = field(init=False)

    def __post_init__(self):
        url = URL.create(
            drivername="mysql+aiomysql",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )

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
