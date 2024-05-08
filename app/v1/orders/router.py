from fastapi import HTTPException, APIRouter, Depends, status;
from ..users.OAuth2 import get_current_user;
from ..users.utils import check_if_admin;
from sqlalchemy.orm import Session;
from ...db.database import get_db;
from ...schemas.orders import *;
from ...models.orders import *;
from .utils import *;


orders_router = APIRouter( tags=["Orders"] );

@orders_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Order_Response)
def create_order(order: Order_Create, user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    cart_items = get_product_items_from_cart(user.id, db)
    
    if cart_items is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty")
    
    order_items = []
    for cart_item in cart_items:
        order_item = OrderItem(
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
        )
        order_items.append(order_item)

    created_order = Order(
        user_id=user.id,
        total_amount=order.total_amount,
        status=order.status,
        country=order.country,
        city=order.city,
        address=order.address,
        order_items=order_items
    )
    db.add(created_order)
    db.commit()
    db.refresh(created_order)

    clear_cart(user.id,db)
    return created_order

@orders_router.get("/", response_model=list[Order_Response],status_code=status.HTTP_200_OK)
def get_all_orders_of_a_user(user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    return orders

@orders_router.get("/orders-all", response_model=list[Order_Response], status_code=status.HTTP_200_OK)
def get_all_orders(user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    check_if_admin(user.id,db)
    orders = db.query(Order).all()
    return orders

@orders_router.get("/{id}", response_model=Order_Response, status_code=status.HTTP_200_OK)
def get_order_by_id(id: int, user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    order = find_order_by_id(id, db)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@orders_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id: int, user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    check_if_admin(user.id,db)
    order = find_order_by_id(id, db)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}