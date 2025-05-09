from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    DateTime, Enum, Numeric
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

# Enum for TransactionType
class TransactionType(enum.Enum):
    INCOME = "Income"
    PAYMENT = "Payment"
    TRANSFER = "Transfer"

# Common timestamp fields
class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

# Asset Types
class AssetType(Base, TimestampMixin):
    __tablename__ = 'asset_types'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    assets = relationship('Asset', back_populates='asset_type')

# Assets (e.g., Bank, Wallet, etc.)
class Asset(Base, TimestampMixin):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    asset_type_id = Column(Integer, ForeignKey('asset_types.id'))

    asset_type = relationship('AssetType', back_populates='assets')
    transactions = relationship('Transaction', back_populates='asset', foreign_keys='Transaction.asset_id')
    received_transactions = relationship('Transaction', foreign_keys='Transaction.destination_asset_id')
    current_sheets = relationship('CurrentSheet', back_populates='asset')

# Expense Categories
class ExpenseType(Base, TimestampMixin):
    __tablename__ = 'expense_types'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    expenses = relationship('Expense', back_populates='expense_type')

# Expenses
class Expense(Base, TimestampMixin):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    description = Column(String, index=True)
    expense_type_id = Column(Integer, ForeignKey('expense_types.id'))

    expense_type = relationship('ExpenseType', back_populates='expenses')
    transactions = relationship('Transaction', back_populates='expense')

# Contact Types (Customer or Vendor)
class ContactType(Base, TimestampMixin):
    __tablename__ = 'contact_types'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    contacts = relationship('Contact', back_populates='contact_type')

# Contacts (Customers or Vendors)
class Contact(Base, TimestampMixin):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    business_name = Column(String, index=True)
    phone = Column(String, index=True)
    description = Column(String)
    contact_type_id = Column(Integer, ForeignKey('contact_types.id'))

    contact_type = relationship('ContactType', back_populates='contacts')
    transactions = relationship('Transaction', back_populates='contact')

# Transactions: Income, Payment, or Transfer
class Transaction(Base, TimestampMixin):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    transaction_type = Column(Enum(TransactionType))
    amount = Column(Numeric(10, 2))
    asset_id = Column(Integer, ForeignKey('assets.id'))  # source asset
    destination_asset_id = Column(Integer, ForeignKey('assets.id'), nullable=True)  # destination asset for transfer
    expense_id = Column(Integer, ForeignKey('expenses.id'), nullable=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=True)
    note = Column(String, index=True)

    asset = relationship('Asset', back_populates='transactions', foreign_keys=[asset_id])
    destination_asset = relationship('Asset', foreign_keys=[destination_asset_id])
    expense = relationship('Expense', back_populates='transactions')
    contact = relationship('Contact', back_populates='transactions')

# Balance tracking for each asset
class CurrentSheet(Base):
    __tablename__ = 'current_sheets'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    balance = Column(Numeric(10, 2))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    asset = relationship('Asset', back_populates='current_sheets')
