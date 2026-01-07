from fastapi import APIRouter, Depends

from app.database.core import get_db_session
from app.schemas.webhook import WebhookPayload
from app.services.transaction import TransactionService

router = APIRouter()


@router.post("/krungthai")
async def krungthai_handler(payload: WebhookPayload, db=Depends(get_db_session)):
    service = TransactionService()
    try:
        await service.process_webhook(db, payload)
        res_json = {"status": "success"}
        print(res_json)
        return res_json
    except Exception as e:
        res_json = {"status": "error", "msg": str(e)}
        print(res_json)
        return res_json
