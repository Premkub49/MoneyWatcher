from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Category
from app.repositories.category import CategoryRepo


class CategoryService:
    def __init__(self):
        self.repo = CategoryRepo()

    async def get_category_by_name(
        self,
        db: AsyncSession,
        category_name: str,
    ) -> Category:
        return await self.repo.get_category_by_name(db, category_name)
