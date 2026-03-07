from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Category


class CategoryRepo:
    async def get_all_categories(self, db: AsyncSession) -> list[Category]:
        """Fetch all categories from DB, ordered by id."""
        stmt = select(Category).order_by(Category.id)
        result = await db.execute(stmt)
        return list(result.scalars().all())

    async def create_category(self, db: AsyncSession, data: Category) -> Category:
        """Insert a new category. Returns the created row with id."""
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return data

    async def delete_category_by_name(self, db: AsyncSession, name: str) -> bool:
        """Delete a category by name. Returns True if deleted."""
        stmt = delete(Category).where(Category.name == name)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0
