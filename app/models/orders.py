from sqlalchemy import Integer, String, Column, Boolean, Float, ForeignKey, DateTime
# from..db.database import Base
from .base import Base
from sqlalchemy.orm import relationship;
from sqlalchemy.sql.expression import text;


class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="orders")
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(String, nullable=False, default='pending')
    country = Column(String, nullable=False)
    city = Column(String,nullable=False)
    address = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('now()'))
    updated_at = Column(DateTime, nullable=False, server_default=text('now()'), onupdate=text('now()'))

    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order", back_populates="order_items")
    product_id = Column(Integer, ForeignKey('products.id'))
    product = relationship("Product", back_populates="order_items")
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False, default=0.0)