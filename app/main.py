from fastapi import FastAPI
from .v1.api import api_v1;
from .db.database import engine;
from .models.users import User;
from .models.products import Product;
from .models.category import Category;
from .models.cart import Cart
from .models.orders import Order,OrderItem


User.metadata.create_all(bind=engine)
Product.metadata.create_all(bind=engine)
Category.metadata.create_all(bind=engine)
Cart.metadata.create_all(bind=engine)
Order.metadata.create_all(bind=engine)
OrderItem.metadata.create_all(bind=engine)

app = FastAPI();


app.include_router(api_v1,prefix="/v1");