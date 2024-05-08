from sqlalchemy import Integer, String, Column, Boolean, Float, ForeignKey, TIMESTAMP
# from..db.database import Base
from .base import Base
from sqlalchemy.sql.expression import text;

class Category(Base):
    __tablename__ = "categories";
    
    id = Column(Integer,index=True,nullable=False,primary_key=True);
    name = Column(String,unique=True,nullable=False);
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'));
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False,server_default=text('now()'));