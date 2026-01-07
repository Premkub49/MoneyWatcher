from sqlalchemy.orm import Session

from app.models.base import Account
from app.repositories.account import AccountRepo


class AccountService:
    def __init__(self):
        self.repo = AccountRepo()

    def get_account(self, db: Session, id=None, account_number=None, provider=None):
        return self.repo.get_account(db, id, account_number, provider)

    def create_account(self, db: Session, data: Account):
        return self.repo.create_account(db, data)
