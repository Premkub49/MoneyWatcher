from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import RawData


class RawDataRepo:
    async def create_raw_data(self, db: AsyncSession, data: RawData) -> RawData:
        """Insert raw data into bronze.raw_data. Returns the created row."""
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return data

    async def get_unprocessed(self, db: AsyncSession) -> list[RawData]:
        """Fetch all unprocessed raw data, ordered by created_at."""
        stmt = select(RawData).where(RawData.is_processed == False).order_by(RawData.created_at).with_for_update()
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, db: AsyncSession, raw_data_id) -> RawData | None:
        """Fetch a single raw data row by id."""
        stmt = select(RawData).where(RawData.id == raw_data_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()

    async def mark_done(self, db: AsyncSession, raw_data_id, status: str) -> RawData | None:
        """Set is_processed = True and process_status for the given raw data id."""
        stmt = select(RawData).where(RawData.id == raw_data_id)
        result = await db.execute(stmt)
        raw = result.scalar_one_or_none()
        if raw:
            raw.is_processed = True
            raw.process_status = status
            await db.commit()
        return raw
