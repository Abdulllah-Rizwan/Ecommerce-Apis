from sqlalchemy import Integer,Column,String,Boolean,TIMESTAMP,ForeignKey;
from sqlalchemy.orm import relationship;
# from..db.database import Base
from .base import Base
from sqlalchemy.sql.expression import text;

class User(Base):
    __tablename__ = "users";
    
    id = Column(Integer,primary_key=True,index=True,nullable=False);
    email = Column(String, unique=True,nullable=False);
    first_name = Column(String,nullable=False);
    last_name = Column(String, nullable=False);
    phone_number = Column(String, nullable=False);
    country_code = Column(String, nullable=False);
    password = Column(String,nullable=False);
    is_admin = Column(Boolean, nullable=False, server_default='false');
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'));
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'), onupdate=text('now()'));
    
    cart = relationship("Cart", back_populates="user", uselist=False);
    orders = relationship("Order", back_populates="user");
     