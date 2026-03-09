import json

from fastapi import APIRouter, BackgroundTasks, Depends

from app.database.core import AsyncSessionLocal, get_db_session
from app.schemas.webhook import WebhookPayload
from app.services.raw_data import RawDataService
from app.services.transaction import TransactionService

router = APIRouter()


async def _process_all_unprocessed():
    """Process all unprocessed raw data (Bronze -> Silver). Runs in background."""
    async with AsyncSessionLocal() as db:
        raw_service = RawDataService()
        tx_service = TransactionService()
        unprocessed = await raw_service.get_unprocessed(db)

        for raw in unprocessed:
            try:
                payload = json.loads(raw.raw_payload)
                category_name = payload.get("category", "Other")
                result = await tx_service.process_raw_data(db, raw.id, category_name)
                status = "success" if result else "failed"
                await raw_service.mark_done(db, raw.id, status)
            except Exception as e:
                await raw_service.mark_done(db, raw.id, "failed")
                print(f"Process raw {raw.id} failed: {e}")


@router.post("/krungthai")
async def krungthai_handler(
    payload: WebhookPayload,
    background_tasks: BackgroundTasks,
    db=Depends(get_db_session),
):
    """Receive MacroDroid webhook. Save to Bronze, then process in background."""
    raw_service = RawDataService()
    await raw_service.save_raw(db, source="Krungthai", payload=payload)
    background_tasks.add_task(_process_all_unprocessed)
    return {"status": "saved"}


@router.post("/process-raw")
async def process_raw_data():
    """Manual trigger: process all unprocessed raw data (Bronze -> Silver)."""
    await _process_all_unprocessed()
    return {"status": "done"}
