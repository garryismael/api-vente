from datetime import date

from pydantic import BaseModel, Field, validator
from src.schemas.product import ProductDb
from src.schemas.user import UserDb


class PurchaseBase(BaseModel):
    quantity: int = Field(..., ge=1)
    product_id: int = Field(..., ge=1)
    
    class Config:
        orm_mode = True

class PurchaseBaseList(BaseModel):
    items: list[PurchaseBase]
    
    @validator('items')
    def items_must(cls, v: list[PurchaseBase]):
        if len(v) <= 0:
            raise ValueError('please make at least one purchase')
        return v
        
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
