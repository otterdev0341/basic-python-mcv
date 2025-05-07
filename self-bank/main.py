import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.server import MCPServer
from src.di_container import DIContainer
from src.infrastructure.mysql.repositories.contact_repo import ContactRepository
from src.application.usecase.contact_usecase import ContactUseCase
from src.infrastructure.http_resources.contact_resources import register_contact_resources
from src.infrastructure.mysql.mysql_connection import MysqlConnection
from src.config.db_config import DbConfig

async def main():
    # Setup DI container
    container = DIContainer()

    # Initialize DB connection
    db_config = DbConfig()
    db = MysqlConnection(db_config)

    # Create and register repository and use case
    contact_repo = ContactRepository(db)
    contact_usecase = ContactUseCase(contact_repo)

    container.register("contact_usecase", contact_usecase)

    # Create MCP server
    mcp = MCPServer(name="Demo", _container=container)

    # Register resources
    register_contact_resources(mcp, contact_usecase)

    # Start the server
    mcp.start()


if __name__ == "__main__":
    asyncio.run(main())
