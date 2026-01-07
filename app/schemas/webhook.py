from pydantic import BaseModel


class WebhookPayload(BaseModel):
    title: str
    notification: str
    category: str
    timestamp: int
