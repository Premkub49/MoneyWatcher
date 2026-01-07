from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Account
from app.repositories.account import AccountRepo


class AccountService:
    def __init__(self):
        self.repo = AccountRepo()

    async def get_account(
        self, db: AsyncSession, id=None, account_number=None, provider=None
    ):
        return await self.repo.get_account(db, id, account_number, provider)

    async def create_account(self, db: AsyncSession, data: Account):
        return await self.repo.create_account(db, data)

    async def create_account_if_not_existed(
        self, db: AsyncSession, account_number: str, provider: str
    ):
        is_account_existed = await self.get_account(
            db, account_number=account_number, provider=provider
        )
        if is_account_existed is None:
            account = Account(
                name=f"{provider} {account_number}",
                account_number=account_number,
                provider=provider,
            )
            await self.create_account(db, data=account)
        return await self.get_account(
            db, account_number=account_number, provider=provider
        )
