from sqlalchemy.orm import Session

from app.models.base import Transaction
from app.repositories.transaction import TransactionRepo


class TransactionService:
    def process_webhook(self, db: Session, payload):
        new_transaction = Transaction()
        repo = TransactionRepo()
        return repo.create_transaction(db, payload)
