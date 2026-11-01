from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class NotificationCreate(BaseModel):
    customer_id: int = Field(gt=0)
    claim_id: int = Field(gt=0)
    message: str = Field(min_length=5, max_length=500)
    notification_type: str = Field(min_length=3, max_length=50)


class NotificationResponse(BaseModel):
    notification_id: int
    customer_id: int
    claim_id: int
    message: str
    notification_type: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)