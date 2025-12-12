from sqlalchemy.orm import Session


class TransactionRepo:
    def create_transaction(self, db: Session, data):
        db.add(data)
        db.commit()
        return data
