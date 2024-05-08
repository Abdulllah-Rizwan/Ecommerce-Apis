from sqlalchemy import Integer, String, Column, Boolean, Float, ForeignKey
# from..db.database import Base
from .base import Base
from sqlalchemy.orm import relationship;


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=False)
    main_image = Column(String, nullable=False)
    sub_images = Column(String, nullable=False)
    
    carts = relationship("Cart", back_populates="product");
    order_items = relationship("OrderItem", back_populates="product");