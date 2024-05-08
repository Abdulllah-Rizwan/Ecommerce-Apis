from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Order_Item_Create(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    
class Order_Create(BaseModel):
    total_amount: float
    status: Optional[str] = "Pending"
    country: str
    city: str
    address: str
    # products: List[Order_Item_Create]

class Order_Item_Response(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
    
class Order_Response(BaseModel):
    id: int
    user_id: int
    total_amount: float
    status: str
    country: str
    city: str
    address: str
    created_at: datetime
    updated_at: datetime
    order_items: List[Order_Item_Response]

class Order_Update(BaseModel):
    total_amount: Optional[float]
    status: Optional[str]
    country: Optional[str]
    city: Optional[str]
    address: Optional[str]

class Order_Item_Update(BaseModel):
    quantity: Optional[int]
    unit_price: Optional[float]