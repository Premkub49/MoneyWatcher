from sqlalchemy.orm import Session

from app.models.base import Account


class AccountRepo:
    def get_account(self, db: Session, id=None, account_number=None, provider=None):
        query = db.query(Account)
        if id:
            query = query.filter(Account.id == id)
        if account_number:
            query = query.filter(Account.account_number == account_number)
        if provider:
            query = query.filter(Account.provider == provider)
        existing_account = query.all()
        return existing_account

    async def create_account(self, db: Session, data: Account):
        db.add(data)
        db.commit()
        return data
