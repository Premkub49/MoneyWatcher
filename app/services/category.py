from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Category
from app.repositories.category import CategoryRepo
from app.services import category_cache as cache


class CategoryService:
    def __init__(self):
        self.repo = CategoryRepo()

    # ── reads (from cache, no DB) ─────────────────────────────

    def get_category_by_name(self, category_name: str):
        """Look up a category by name from cache. Returns entry or None."""
        return cache.get_by_name(category_name)

    def get_all_categories(self):
        """Get all categories from cache."""
        return cache.get_all()

    # ── writes (DB + update cache) ────────────────────────────

    async def create_category(
        self, db: AsyncSession, name: str, display_name: str, cat_type: str
    ) -> Category:
        """Create a new category in DB and add to cache. Raises ValueError if name exists."""
        if cache.get_by_name(name):
            raise ValueError(f"Category '{name}' already exists")

        new_cat = Category(name=name, display_name=display_name, type=cat_type)
        saved = await self.repo.create_category(db, new_cat)
        cache.add_to_cache(saved)
        return saved

    async def delete_category(self, db: AsyncSession, name: str) -> bool:
        """Delete a category from DB and remove from cache. Returns True if deleted."""
        deleted = await self.repo.delete_category_by_name(db, name)
        if deleted:
            cache.remove_from_cache(name)
        return deleted

    async def load_cache(self, db: AsyncSession) -> None:
        """Load all categories from DB into cache (called at startup)."""
        categories = await self.repo.get_all_categories(db)
        cache.load_cache(categories)
