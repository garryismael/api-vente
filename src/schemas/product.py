from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: int = Field(..., gt=0)
    stock: int = Field(..., gt=1)
    
    class Config:
        orm_mode = True
        
        
class ProductDb(ProductBase):
    id: int
