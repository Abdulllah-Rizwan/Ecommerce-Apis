from pydantic import BaseModel,EmailStr;
from datetime import datetime;
from typing import Optional;


class User_Create(BaseModel):
    first_name: str;
    last_name: str;
    phone_number: str;
    country_code: str;
    email: EmailStr;
    password: str;
    is_admin: Optional[bool] = False;
    
class User_Out(BaseModel):
    id: int;
    first_name: str;
    last_name: str;
    phone_number: str;
    country_code: str;
    email: EmailStr;
    is_admin: bool;
    created_at: datetime;
    updated_at: datetime;

class Update_User(BaseModel):
    id:int;
    old_password: str;
    new_password:str;
    
class Token(BaseModel):
    token:str;
    token_type:str

class Token_Data(BaseModel):
    id: Optional[str] = None