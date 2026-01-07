from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Category


class CategoryRepo:
    async def get_category_by_name(self, db: AsyncSession, category_name: str):
        stmt = select(Category).where(Category.name == category_name)
        result = await db.execute(stmt)
        category = result.scalar_one_or_none()
        return category
