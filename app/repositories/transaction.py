from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Transaction


class TransactionRepo:
    async def create_transaction(self, db: AsyncSession, data: Transaction):
        """Insert a transaction into DB."""
        db.add(data)
        await db.commit()
        return data
