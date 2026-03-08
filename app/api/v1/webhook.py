import json

from fastapi import APIRouter, Depends

from app.database.core import get_db_session
from app.schemas.webhook import WebhookPayload
from app.services.raw_data import RawDataService
from app.services.transaction import TransactionService

router = APIRouter()


@router.post("/krungthai")
async def krungthai_handler(payload: WebhookPayload, db=Depends(get_db_session)):
    """Receive Macrodroid webhook, save to Bronze, then process to Transaction (Silver)."""
    # service = TransactionService()
    raw_service = RawDataService()
    try:
        # result = await service.process_webhook(
        #     db, source="Krungthai", payload=payload, category_name=payload.category
        # )
        # if result is None:
        #     return {"status": "skipped", "msg": "amount is 0, not added"}
        # return {"status": "success"}
        await raw_service.save_raw(db, source="Krungthai", payload=payload)
        return {"status": "saved"}
    except Exception as e:
        return {"status": "error", "msg": str(e)}


@router.post("/process-raw")
async def process_raw_data(db=Depends(get_db_session)):
    """Process all unprocessed raw data (Bronze -> Silver). Returns processed count and results."""
    raw_service = RawDataService()
    tx_service = TransactionService()
    unprocessed = await raw_service.get_unprocessed(db)

    results = []
    for raw in unprocessed:
        try:
            payload = json.loads(raw.raw_payload)
            category_name = payload.get("category", "Other")
            result = await tx_service.process_raw_data(db, raw.id, category_name)
            results.append({"id": str(raw.id), "status": "processed" if result else "skipped"})
        except Exception as e:
            results.append({"id": str(raw.id), "status": "error", "msg": str(e)})

    return {"processed": len(results), "results": results}
