from fastapi import HTTPException,APIRouter,Response,Depends,status;
from ..users.OAuth2 import get_current_user;
from ..users.utils import check_if_admin;
from ...models.category import Category;
from sqlalchemy.orm import Session;
from ...db.database import get_db;
from ...schemas.category import *;

category_router = APIRouter( tags=["Categories"] );

@category_router.post("/",status_code=status.HTTP_201_CREATED,response_model=Category_Out)
def create_category(category:Create_Category, db:Session = Depends(get_db),user: int = Depends(get_current_user)):
    check_if_admin(user.id,db)
    if db.query(Category).filter(category.name == Category.name).first():
        raise HTTPException(status.HTTP_409_CONFLICT,detail="Category already exists")
    created_category = Category(**category.model_dump());
    db.add(created_category);
    db.commit();
    db.refresh(created_category);
    return created_category;

@category_router.get("/", status_code=status.HTTP_200_OK, response_model=list[Category_Out])
def get_all_categories(db:Session = Depends(get_db)):
    categories = db.query(Category).all();
    return categories;

@category_router.patch('/',status_code=status.HTTP_200_OK,response_model=Category_Out)
def update_categorty(category_update_data: Update_Category ,db: Session = Depends(get_db),user: int = Depends(get_current_user)):
    check_if_admin(user.id,db)
    category_to_be_updated = db.query(Category).filter(category_update_data.id == Category.id).first()
    if not category_to_be_updated:
        raise HTTPException(status.HTTP_204_NO_CONTENT,detail = "No such contegory exists");
    db.query(Category).filter(category_update_data.id == Category.id).update(category_update_data.dict(exclude_unset=True))
    db.commit();
    db.refresh(category_to_be_updated);
    return category_to_be_updated;

@category_router.delete('/{category_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db),user: int = Depends(get_current_user)):
    check_if_admin(user.id,db)
    category_to_be_deleted= db.query(Category).get(category_id);
    if not category_to_be_deleted: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such category exists.");
    db.delete(category_to_be_deleted)
    db.commit();
    return Response(status_code=status.HTTP_204_NO_CONTENT);