from sqlalchemy import select

from app.database.core import AsyncSessionLocal, Base, async_engine
from app.models.base import Category
from app.models.enums import CategoryType

DEFAULT_CATEGORIES = [
    {"name": "Food", "type": CategoryType.EXPENSE},
    {"name": "Travel", "type": CategoryType.EXPENSE},
    {"name": "Shopping", "type": CategoryType.EXPENSE},
    {"name": "Bill", "type": CategoryType.EXPENSE},
    {"name": "Transfer", "type": CategoryType.TRANSFER},
]


async def init_master_data():
    print("Checking master data...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with AsyncSessionLocal() as session:
        for cat_data in DEFAULT_CATEGORIES:
            stmt = select(Category).where(Category.name == cat_data["name"])
            result = await session.execute(stmt)
            existing_cat = result.scalar_one_or_none()

            if not existing_cat:
                new_cat = Category(name=cat_data["name"], type=cat_data["type"])
                session.add(new_cat)
                print(f"Created default category: {cat_data['name']}")
            else:
                pass

        await session.commit()
        print("Master data initialization complete.")
