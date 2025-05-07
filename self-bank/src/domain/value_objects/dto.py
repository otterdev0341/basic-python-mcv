from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum
from decimal import Decimal

# --- ENUMS ---
class TransactionTypeEnum(str, Enum):
    INCOME = "Income"
    PAYMENT = "Payment"

# === ASSET TYPE DTOs ===
class CreateAssetTypeDto(BaseModel):
    name: str

class UpdateAssetTypeDto(BaseModel):
    name: Optional[str] = None

class ResAssetTypeDto(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes = True

# === ASSET DTOs ===
class CreateAssetDto(BaseModel):
    name: str
    asset_type_id: int

class UpdateAssetDto(BaseModel):
    name: Optional[str] = None
    asset_type_id: Optional[int] = None

class ResAssetDto(BaseModel):
    id: int
    name: str
    asset_type_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# === EXPENSE TYPE DTOs ===
class CreateExpenseTypeDto(BaseModel):
    name: str

class UpdateExpenseTypeDto(BaseModel):
    name: Optional[str] = None

class ResExpenseTypeDto(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# === EXPENSE DTOs ===
class CreateExpenseDto(BaseModel):
    description: str
    expense_type_id: int

class UpdateExpenseDto(BaseModel):
    description: Optional[str] = None
    expense_type_id: Optional[int] = None

class ResExpenseDto(BaseModel):
    id: int
    description: str
    expense_type_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# === CONTACT TYPE DTOs ===
class CreateContactTypeDto(BaseModel):
    name: str

class UpdateContactTypeDto(BaseModel):
    name: Optional[str] = None

class ResContactTypeDto(BaseModel):
    id: int
    name: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# === CONTACT DTOs ===
class CreateContactDto(BaseModel):
    name: str
    business_name: str
    phone: str
    description: Optional[str] = None
    contact_type_id: int

class UpdateContactDto(BaseModel):
    name: Optional[str] = None
    business_name: Optional[str] = None
    phone: Optional[str] = None
    description: Optional[str] = None
    contact_type_id: Optional[int] = None

class ResContactDto(BaseModel):
    id: int
    name: str
    business_name: str
    phone: str
    description: Optional[str]
    contact_type_id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# === TRANSACTION DTOs ===
class CreateTransactionDto(BaseModel):
    transaction_type: TransactionTypeEnum
    amount: Decimal
    asset_id: int
    expense_id: Optional[int] = None
    contact_id: Optional[int] = None
    note: Optional[str] = None

class UpdateTransactionDto(BaseModel):
    transaction_type: Optional[TransactionTypeEnum] = None
    amount: Optional[Decimal] = None
    asset_id: Optional[int] = None
    expense_id: Optional[int] = None
    contact_id: Optional[int] = None
    note: Optional[str] = None

class ResTransactionDto(BaseModel):
    id: int
    transaction_type: TransactionTypeEnum
    amount: Decimal
    asset_id: int
    expense_id: Optional[int]
    contact_id: Optional[int]
    note: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True

# === CURRENT SHEET DTOs ===
class CreateCurrentSheetDto(BaseModel):
    asset_id: int
    balance: Decimal

class UpdateCurrentSheetDto(BaseModel):
    balance: Optional[Decimal] = None

class ResCurrentSheetDto(BaseModel):
    id: int
    asset_id: int
    balance: Decimal
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
