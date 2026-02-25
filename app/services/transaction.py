import re

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Transaction
from app.repositories.transaction import TransactionRepo
from app.schemas.webhook import WebhookPayload
from app.services.account import AccountService
from app.services.category import CategoryService


class TransactionService:
    def __init__(self):
        self.repo = TransactionRepo()
        self.account_service = AccountService()
        self.category_service = CategoryService()

    async def process_webhook(self, db: AsyncSession, payload: WebhookPayload):
        text = payload.notification
        print(payload)
        provider_match = re.search(r"(Krungthai)", payload.title, re.IGNORECASE)
        provider = provider_match.group(1) if provider_match else "Not found krungthai"
        acc_match = re.search(r"บัญชี\s+(\w+)", text)
        account_number = acc_match.group(1) if acc_match else "Not found account number"

        account_data = await self.account_service.create_account_if_not_existed(
            db, provider=provider, account_number=account_number
        )

        category = await self.category_service.get_category_by_name(
            db, payload.category
        )

        type_match = re.search(r"เงิน(.*?):", text)
        raw_type = type_match.group(1) if type_match else ""

        if raw_type == "เข้า":
            action_type = "income"
        elif raw_type == "ออก":
            action_type = "expense"
        else:
            action_type = "none"

        amount_match = re.search(r"(-?[\d,]+\.\d{2})\s+บาท", text)
        amount = float(amount_match.group(1)) if amount_match else 0

        await self.account_service.update_balance_account(db, account_data.id, account_data.balance + amount)

        new_transaction = Transaction(
            account_id=account_data.id,
            category_id=category.id,
            type=action_type,
            amount=amount,
            note=payload.notification,
            bank_timestamp=str(payload.timestamp),
        )
        return await self.create_transaction(db, new_transaction)

    async def create_transaction(self, db: AsyncSession, transaction: Transaction):
        return await self.repo.create_transaction(db, transaction)
