from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Account


class AccountRepo:
    async def get_account(
        self, db: AsyncSession, id=None, account_number=None, provider=None
    ):
        stmt = select(Account)
        if id:
            stmt = stmt.where(Account.id == id)
        if account_number:
            stmt = stmt.where(Account.account_number == account_number)
        if provider:
            stmt = stmt.where(Account.provider == provider)
        result = await db.execute(stmt)
        existing_account = result.scalars().all()
        return existing_account

    async def create_account(self, db: AsyncSession, data: Account):
        db.add(data)
        await db.commit()
        return data
