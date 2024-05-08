from fastapi import APIRouter;
from .users.router import user_router
from .products.router import product_router
from .cart.router import cart_router
from .category.router import category_router
from .orders.router import orders_router

api_v1 = APIRouter();

api_v1.include_router( user_router, prefix = '/users' )
api_v1.include_router( product_router, prefix = '/products' )
api_v1.include_router( category_router, prefix = '/category' )
api_v1.include_router( cart_router, prefix = '/cart' )
api_v1.include_router( orders_router, prefix = '/orders' )