import json

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import RawData
from app.repositories.raw_data import RawDataRepo
from app.schemas.webhook import WebhookPayload


class RawDataService:
    """Bronze layer service — stores raw webhook payloads."""

    def __init__(self):
        self.repo = RawDataRepo()

    async def save_raw(self, db: AsyncSession, source: str, payload: WebhookPayload) -> RawData:
        """Save raw payload to bronze.raw_data. Returns the created row."""
        raw = RawData(
            source=source,
            raw_payload=json.dumps(payload.model_dump(), ensure_ascii=False),
        )
        return await self.repo.create_raw_data(db, raw)

    async def get_unprocessed(self, db: AsyncSession) -> list[RawData]:
        """Get all unprocessed raw data rows."""
        return await self.repo.get_unprocessed(db)

    async def mark_done(self, db: AsyncSession, raw_data_id, status: str):
        """Mark a raw data row as processed with status (success/failed)."""
        return await self.repo.mark_done(db, raw_data_id, status)
