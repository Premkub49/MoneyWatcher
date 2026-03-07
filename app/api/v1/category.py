from fastapi import APIRouter, Depends, HTTPException

from app.database.core import get_db_session
from app.schemas.webhook import CategoryResponse, CreateCategoryRequest
from app.services.category import CategoryService

router = APIRouter()
service = CategoryService()

DEFAULT_CATEGORIES = {"Food", "Travel", "Shopping", "Bill", "Transfer IN", "Transfer OUT", "Other"}


@router.get("/", response_model=list[CategoryResponse])
async def list_categories():
    """Get all categories from cache. Returns list[CategoryResponse]."""
    categories = service.get_all_categories()
    return [
        CategoryResponse(
            id=cat.id,
            name=cat.name,
            display_name=cat.display_name,
            type=cat.type.value,
        )
        for cat in categories
    ]


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(body: CreateCategoryRequest, db=Depends(get_db_session)):
    """Create a new category. Input: CreateCategoryRequest. Returns CategoryResponse. 409 if name exists."""
    try:
        cat = await service.create_category(db, body.name, body.display_name, body.type)
        return CategoryResponse(
            id=cat.id,
            name=cat.name,
            display_name=cat.display_name,
            type=cat.type.value if hasattr(cat.type, "value") else cat.type,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/{category_name}", status_code=200)
async def delete_category(category_name: str, db=Depends(get_db_session)):
    """Delete a category by name. 400 if default, 404 if not found."""
    if category_name in DEFAULT_CATEGORIES:
        raise HTTPException(status_code=400, detail=f"Cannot delete default category '{category_name}'")

    deleted = await service.delete_category(db, category_name)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Category '{category_name}' not found")
    return {"status": "deleted", "name": category_name}
