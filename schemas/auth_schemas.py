from pydantic import BaseModel
from typing import Optional
from dynaconf import settings

class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    password: str 
    email: str
    is_active: Optional[bool]
    is_staff: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "johndoe",
                "password": "123456",
                "email": "johndoe@gmail.com",
                "is_active": False,
                "is_staff": False,
            }
        }

class Settings(BaseModel):
    authjwt_secret_key: str = settings.AUTHJWT_SECRET_KEY

class LoginModel(BaseModel):
    username: str
    password: str        