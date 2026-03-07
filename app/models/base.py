import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, event, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import UniqueConstraint

from app.database.core import Base

from .enums import CategoryType


# ── Default categories (seeded when table is created) ─────────

DEFAULT_CATEGORIES = [
    {"name": "Food",         "display_name": "🍔 Food",         "type": "EXPENSE"},
    {"name": "Travel",       "display_name": "🚗 Travel",       "type": "EXPENSE"},
    {"name": "Shopping",     "display_name": "🛒 Shopping",     "type": "EXPENSE"},
    {"name": "Bill",         "display_name": "📄 Bill",         "type": "EXPENSE"},
    {"name": "Transfer IN",  "display_name": "📥 Transfer IN",  "type": "INCOME"},
    {"name": "Transfer OUT", "display_name": "📤 Transfer OUT", "type": "EXPENSE"},
    {"name": "Other",        "display_name": "📦 Other",        "type": "OTHER"},
]


# ── Bronze Layer (schema: bronze) ─────────────────────────────

class RawData(Base):
    __tablename__ = "raw_data"
    __table_args__ = {"schema": "bronze"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String(100), nullable=False)          # bank name
    raw_payload = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_processed = Column(Boolean, default=False)          # processed flag


# ── Silver Layer (schema: public) ────────────────────────────

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    account_number = Column(String(50))
    provider = Column(String(50))
    balance = Column(Float, default=0.00)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    transactions = relationship("Transaction", back_populates="account")

    __table_args__ = (
        UniqueConstraint("account_number", "provider", name="uix_account_provider"),
    )


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    display_name = Column(String(150), nullable=False)     # emoji + name
    type = Column(Enum(CategoryType), nullable=False)

    transactions = relationship("Transaction", back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    amount = Column(Float, nullable=False)
    bank_timestamp = Column(String(50), nullable=True)
    note = Column(String, nullable=True)               # used when category is Other
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    account = relationship("Account", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")


# ── Seed default categories after table creation ──────────────

def _seed_categories(target, connection, **kwargs):
    """Insert default categories when the categories table is first created."""
    for cat in DEFAULT_CATEGORIES:
        connection.execute(
            target.insert().values(
                name=cat["name"],
                display_name=cat["display_name"],
                type=cat["type"],
            )
        )

event.listen(Category.__table__, "after_create", _seed_categories)
