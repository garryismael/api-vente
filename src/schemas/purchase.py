from datetime import date

from pydantic import BaseModel, Field
from src.schemas.product import ProductDb
from src.schemas.user import UserDb


class PurchaseBase(BaseModel):
    quantity: int = Field(..., gt=1)
    product_id: int = Field(..., gt=1)
    
    class Config:
        orm_mode = True

class PurchaseCreate(PurchaseBase):
    user_id: int = Field(..., gt=1)
    quantity: int = Field(..., gt=1)

class PurchaseDb(PurchaseBase):
    id: int
    client: UserDb
    product: ProductDb
    date_purchase: date
