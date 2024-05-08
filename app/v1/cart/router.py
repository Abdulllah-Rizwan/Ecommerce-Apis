from fastapi import HTTPException, APIRouter, Depends, status;
from ..users.OAuth2 import get_current_user;
from ..users.utils import check_if_admin;
from ...models.products import Product;
from sqlalchemy.orm import Session;
from ...db.database import get_db;
from ...models.cart import Cart;
from ...schemas.cart import *;
from typing import List;

cart_router = APIRouter( tags=["Cart"] );

@cart_router.get("/all-carts", response_model=List[Cart_Response],status_code = status.HTTP_200_OK)
def get_all_cart(db: Session = Depends(get_db), user: int = Depends(get_current_user),Limit:int = 10,skip: int = 0):
    check_if_admin(user.id,db)
    cart = db.query(Cart).limit(Limit).offset(skip).all()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found");
    return cart;

@cart_router.get("/", response_model=List[Cart_Response],status_code = status.HTTP_200_OK)
def get_my_carts(db:Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).all();
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found");
    return cart;

@cart_router.post("/", response_model=Cart_Response, status_code = status.HTTP_201_CREATED)
def create_cart(cart: Cart_Request, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == cart.product_id).first();
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found");
    cart = Cart(user_id = current_user.id, product_id = cart.product_id,quantity = cart.quantity,unit_price = product.price);
    db.add(cart);
    db.commit();
    db.refresh(cart);
    return cart;

@cart_router.delete("/", status_code = status.HTTP_204_NO_CONTENT)
def delete_cart(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first();
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found");
    db.delete(cart);
    db.commit();
    return {"message": "Cart deleted successfully"};