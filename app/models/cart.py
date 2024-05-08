from sqlalchemy import Integer,Column,String,Boolean,TIMESTAMP,ForeignKey,Float;
from sqlalchemy.orm import relationship;
# from..db.database import Base
from .base import Base
class Cart(Base):
    __tablename__ = "carts";
    id = Column(Integer,primary_key=True,index=True);
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False);
    user = relationship("User",back_populates="cart", uselist=False);
    product_id = Column(Integer,ForeignKey("products.id"),nullable=False);
    product = relationship("Product",back_populates="carts");
    quantity = Column(Integer,default=1)
    unit_price = Column(Float, nullable=False ,default=0.0)