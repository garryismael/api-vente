from pydantic import BaseModel, Field, validator
from src.utils.product import allowed_file


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: int = Field(..., gt=1)
    description: str = Field(..., min_length=3)
    image: str
    class Config:
        orm_mode = True
    
    @validator('image')
    def email_must_be_unique(cls, v):
        if not allowed_file(v):
            raise ValueError('file not allowed')
        return v
        
class ProductDb(ProductBase):
    id: int
