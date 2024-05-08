
from pydantic import BaseModel
from typing import Optional
from typing import List
from fastapi import UploadFile


class Create_Product(BaseModel):
    name: str
    price: float
    stock: int
    category: str
    description: str

class Image_Response(BaseModel):
    filename: str
    url: str
    
class Products_Response(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    category: str
    description: str
    main_image: Image_Response
    sub_images: List[Image_Response]
    
class Product_Response(BaseModel):
    message: str
    product_id: int

class Updated_Product_Response(Product_Response):
    updated_product: dict

class Product_Update_Request(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    category: Optional[str] = None
    description: Optional[str] = None
    main_image: Optional[UploadFile] = None
    sub_images: Optional[List[UploadFile]] = None
