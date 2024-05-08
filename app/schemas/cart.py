from pydantic import BaseModel


class Cart_Request(BaseModel):
    quantity: int
    product_id: int

class Cart_Response(Cart_Request):
    id: int
    user_id:int
    unit_price:float
    
    
    class Config:
        orm_mode = True