from sqlalchemy import select

from app.database.core import AsyncSessionLocal
from app.models.base import Category, DEFAULT_CATEGORIES
from app.models.enums import CategoryType
from app.services import category_cache as cache


async def init_master_data():
    """Load categories into cache. If DB is empty, seed defaults first."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Category).order_by(Category.id))
        categories = list(result.scalars().all())

        # seed if table is empty
        if not categories:
            print("No categories found, seeding defaults...")
            for cat in DEFAULT_CATEGORIES:
                session.add(Category(
                    name=cat["name"],
                    display_name=cat["display_name"],
                    type=CategoryType(cat["type"].lower()),
                ))
            await session.commit()

            result = await session.execute(select(Category).order_by(Category.id))
            categories = list(result.scalars().all())

        cache.load_cache(categories)
    print("Category cache loaded.")
