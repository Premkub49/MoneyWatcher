from typing import Optional

from pydantic import BaseModel


class WebhookPayload(BaseModel):
    """Raw payload from Macrodroid webhook."""
    title: str
    notification: str
    category: str
    timestamp: int
    note: Optional[str] = None      # ใช้เมื่อ category เป็น Other (ให้พิมพ์เพิ่ม)


class ProcessPayload(BaseModel):
    """Payload for triggering raw data processing."""
    raw_data_id: str
    category: str


class CategoryResponse(BaseModel):
    """Response schema for category list API."""
    id: int
    name: str
    display_name: str
    type: str


class CreateCategoryRequest(BaseModel):
    """Request body for creating a new category."""
    name: str
    display_name: str
    type: str  # INCOME / EXPENSE / OTHER
