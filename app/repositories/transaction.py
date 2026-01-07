from sqlalchemy.orm import Session

from app.models.base import Transaction


class TransactionRepo:
    def create_transaction(self, db: Session, data: Transaction):
        db.add(data)
        db.commit()
        return data
