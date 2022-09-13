from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    address: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    password: str
    
class UserDb(UserBase):
    id: int
    is_admin: bool
    