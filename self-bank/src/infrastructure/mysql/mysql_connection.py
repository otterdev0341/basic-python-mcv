from dataclasses import dataclass, field
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
)
from sqlalchemy.engine import URL
from src.config.db_config import DbConfig
from sqlalchemy.orm import declarative_base
Base = declarative_base()


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

    async def dispose(self) -> None:
        """
        Disposes the engine and releases any resources held by it.
        Should be called when the application shuts down.
        """
        if self.engine:
            try:
                await self.engine.dispose()
            except Exception as e:
                print(f"Error disposing engine: {e}")
    
    async def create_tables(self) -> None:
        """
        Creates the tables in the database based on the current models.
        This method uses SQLAlchemy's `Base.metadata.create_all()` to create tables.
        """
        try:
            async with self.engine.begin() as conn:
                # This creates the tables in the database
                await conn.run_sync(Base.metadata.create_all)
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
