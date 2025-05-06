from sqlalchemy import  Column, Integer, String, ForeignKey, DateTime, Enum, Decimal
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()

# Enum for TransactionType
class TransactionType(enum.Enum):
    INCOME = "Income"
    PAYMENT = "Payment"

class AssetType(Base):
    __tablename__ = 'asset_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # One-to-many relationship with Asset
    assets = relationship('Asset', back_populates='asset_type')


class Asset(Base):
    __tablename__ = 'assets'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    asset_type_id = Column(Integer, ForeignKey('asset_types.id'))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Many-to-one relationship with AssetType
    asset_type = relationship('AssetType', back_populates='assets')

    # One-to-many relationship with Transaction
    transactions = relationship('Transaction', back_populates='asset')

    # One-to-many relationship with CurrentSheet
    current_sheets = relationship('CurrentSheet', back_populates='asset')


class ExpenseType(Base):
    __tablename__ = 'expense_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # One-to-many relationship with Expense
    expenses = relationship('Expense', back_populates='expense_type')


class Expense(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    expense_type_id = Column(Integer, ForeignKey('expense_types.id'))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Many-to-one relationship with ExpenseType
    expense_type = relationship('ExpenseType', back_populates='expenses')

    # One-to-many relationship with Transaction
    transactions = relationship('Transaction', back_populates='expense')


class CustomerType(Base):
    __tablename__ = 'customer_types'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)  # 'Customer' or 'Vendor'
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # One-to-many relationship with Contact
    contacts = relationship('Contact', back_populates='customer_type')


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    business_name = Column(String, index=True)
    phone = Column(String, index=True)
    description = Column(String)
    customer_type_id = Column(Integer, ForeignKey('customer_types.id'))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Many-to-one relationship with CustomerType
    customer_type = relationship('CustomerType', back_populates='contacts')

    # One-to-many relationship with Transaction
    transactions = relationship('Transaction', back_populates='contact')


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    transaction_type = Column(Enum(TransactionType))
    amount = Column(Decimal(10, 2))
    asset_id = Column(Integer, ForeignKey('assets.id'))
    expense_id = Column(Integer, ForeignKey('expenses.id'), nullable=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=True)
    note = Column(String, index=True)

    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    # Many-to-one relationship with Asset
    asset = relationship('Asset', back_populates='transactions')

    # Many-to-one relationship with Expense
    expense = relationship('Expense', back_populates='transactions')

    # Many-to-one relationship with Contact
    contact = relationship('Contact', back_populates='transactions')


class CurrentSheet(Base):
    __tablename__ = 'current_sheets'

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey('assets.id'))
    balance = Column(Decimal(10, 2))
    updated_at = Column(DateTime)

    # Many-to-one relationship with Asset
    asset = relationship('Asset', back_populates='current_sheets')
