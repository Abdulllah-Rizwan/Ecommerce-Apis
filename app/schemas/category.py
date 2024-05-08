from pydantic import BaseModel
from datetime import datetime

class Create_Category(BaseModel):
    name: str

class Category_Out(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
    
class Update_Category(BaseModel):
    id: str
    name: str