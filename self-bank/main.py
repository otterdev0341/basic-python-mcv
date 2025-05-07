import sys
import os
import asyncio
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from src.server import MCPServer
from src.di_container import DIContainer
from src.infrastructure.mysql.mysql_connection import MysqlConnection
from src.config.db_config import DbConfig

# Import repositories
from src.infrastructure.mysql.repositories.contact_repo import ContactRepository
from src.infrastructure.mysql.repositories.contact_type_repo import ContactTypeRepository
from src.infrastructure.mysql.repositories.expense_repo import ExpenseRepository
from src.infrastructure.mysql.repositories.expense_type_repo import ExpenseTypeRepository
from src.infrastructure.mysql.repositories.assest_repo import AssetRepository
from src.infrastructure.mysql.repositories.assest_type_repo import AssetTypeRepository
from src.infrastructure.mysql.repositories.transaction_repo import TransactionRepository
from src.infrastructure.mysql.repositories.tranfer_repo import TransferRepository

# Import usecases
from src.application.usecase.contact_usecase import ContactUseCase
from src.application.usecase.contact_type_usecase import ContactTypeUseCase
from src.application.usecase.expense_usecase import ExpenseUseCase
from src.application.usecase.expense_type_usecase import ExpenseTypeUseCase
from src.application.usecase.assest_usecase import AssetUseCase
from src.application.usecase.assest_type_usecase import AssetTypeUseCase
from src.application.usecase.transaction_usecase import TransactionUseCase
from src.application.usecase.tranfer_usecase import TransferUseCase

# Import resource registrations
from src.infrastructure.http_resources.contact_resources import register_contact_resources
from src.infrastructure.http_resources.expense_resources import register_expense_resources
from src.infrastructure.http_resources.expense_type_resources import register_expense_type_resources
from src.infrastructure.http_resources.asset_resources import register_asset_resources
from src.infrastructure.http_resources.transaction_resources import register_transaction_resources
from src.infrastructure.http_resources.transfer_resources import register_transfer_resources

async def main():
    # Setup DI container
    container = DIContainer()

    # Initialize DB connection
    db_config = DbConfig()
    db = MysqlConnection(db_config)

    # Migrate all Schema
    await db.create_tables()

    # Create and register repositories
    contact_repo = ContactRepository(db)
    contact_type_repo = ContactTypeRepository(db)
    expense_repo = ExpenseRepository(db)
    expense_type_repo = ExpenseTypeRepository(db)
    asset_repo = AssetRepository(db)
    asset_type_repo = AssetTypeRepository(db)
    transaction_repo = TransactionRepository(db)
    transfer_repo = TransferRepository(db)

    # Create and register usecases
    contact_usecase = ContactUseCase(contact_repo)
    contact_type_usecase = ContactTypeUseCase(contact_type_repo)
    expense_usecase = ExpenseUseCase(expense_repo)
    expense_type_usecase = ExpenseTypeUseCase(expense_type_repo)
    asset_usecase = AssetUseCase(asset_repo)
    asset_type_usecase = AssetTypeUseCase(asset_type_repo)
    transaction_usecase = TransactionUseCase(transaction_repo)
    transfer_usecase = TransferUseCase(transfer_repo)

    # Register usecases in container
    container.register("contact_usecase", contact_usecase)
    container.register("contact_type_usecase", contact_type_usecase)
    container.register("expense_usecase", expense_usecase)
    container.register("expense_type_usecase", expense_type_usecase)
    container.register("asset_usecase", asset_usecase)
    container.register("asset_type_usecase", asset_type_usecase)
    container.register("transaction_usecase", transaction_usecase)
    container.register("transfer_usecase", transfer_usecase)

    # Create MCP server
    mcp = MCPServer(name="self-money-habbit", _container=container)

    # Register resources
    register_contact_resources(mcp, contact_usecase)
    register_expense_resources(mcp, expense_usecase)
    register_expense_type_resources(mcp, expense_type_usecase)
    register_asset_resources(mcp, asset_usecase)
    register_transaction_resources(mcp, transaction_usecase)
    register_transfer_resources(mcp, transfer_usecase)

    # Start the server
    mcp.start()


if __name__ == "__main__":
    asyncio.run(main())
