from pydantic import BaseModel, Field
from src.schemas.product import ProductDb
from src.schemas.user import UserDb


class OrderBase(BaseModel):
    quantity: int = Field(..., gt=1)
    
    class Config:
        orm_mode = True
    
class OrderCreate(OrderBase):
    product: int

class OrderDb(OrderCreate):
    id: int
    client: UserDb
    product: ProductDb
