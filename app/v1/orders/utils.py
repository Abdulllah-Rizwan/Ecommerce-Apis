from sqlalchemy.orm import Session
from ...models.cart import Cart
from ...models.orders import Order
from fastapi import HTTPException,status
import httpx


def get_product_items_from_cart(user_id,db:Session):
    return db.query(Cart).filter(Cart.user_id == user_id).all() or None

def clear_cart(user_id,db:Session):
    cart = db.query(Cart).filter(Cart.user_id == user_id).all()
    if cart:
        for cart_item in cart:
            db.delete(cart_item)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    
def find_order_by_id(order_id,db:Session):
    return db.query(Order).filter(Order.id == order_id).first()

