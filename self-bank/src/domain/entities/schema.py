from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

# Enum for TransactionType
class TransactionType(enum.Enum):
    INCOME = "Income"
    PAYMENT = "Payment"

class TimestampMixin:
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

class AssetType(Base, TimestampMixin):
    __tablename__ = 'asset_types'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    assets = relationship('Asset', back_populates='asset_type')

class Asset(Base, TimestampMixin):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    asset_type_id = Column(Integer, ForeignKey('asset_types.id'))
    asset_type = relationship('AssetType', back_populates='assets')
    transactions = relationship('Transaction', back_populates='asset')
    current_sheets = relationship('CurrentSheet', back_populates='asset')

class ExpenseType(Base, TimestampMixin):
    __tablename__ = 'expense_types'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    expenses = relationship('Expense', back_populates='expense_type')

class Expense(Base, TimestampMixin):
    __tablename__ = 'expenses'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    description = Column(String, index=True)
    expense_type_id = Column(Integer, ForeignKey('expense_types.id'))
    expense_type = relationship('ExpenseType', back_populates='expenses')
    transactions = relationship('Transaction', back_populates='expense')

class CustomerType(Base, TimestampMixin):
    __tablename__ = 'customer_types'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    contacts = relationship('Contact', back_populates='customer_type')

class Contact(Base, TimestampMixin):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, index=True)
    business_name = Column(String, index=True)
    phone = Column(String, index=True)
    description = Column(String)
    customer_type_id = Column(Integer, ForeignKey('customer_types.id'))
    customer_type = relationship('CustomerType', back_populates='contacts')
    transactions = relationship('Transaction', back_populates='contact')

class Transaction(Base, TimestampMixin):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    transaction_type = Column(Enum(TransactionType))
    amount = Column(Numeric(10, 2))
    asset_id = Column(Integer, ForeignKey('assets.id'))
    expense_id = Column(Integer, ForeignKey('expenses.id'), nullable=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=True)
    note = Column(String, index=True)
    asset = relationship('Asset', back_populates='transactions')
    expense = relationship('Expense', back_populates='transactions')
    contact = relationship('Contact', back_populates='transactions')

class CurrentSheet(Base):
    __tablename__ = 'current_sheets'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    balance = Column(Numeric(10, 2))
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    asset = relationship('Asset', back_populates='current_sheets')
