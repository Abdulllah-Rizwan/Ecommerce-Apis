from fastapi import HTTPException, APIRouter, Depends, status, File, UploadFile, Form;
from..users.OAuth2 import get_current_user;
from ..users.utils import check_if_admin;
from sqlalchemy.orm import Session;
from...db.database import get_db;
from...schemas.products import *;
from...models.products import *;
from.utils import *;
import shutil;
import os;


product_router = APIRouter( tags=["Products"] )

@product_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Product_Response)
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    category: str = Form(...),
    description: str = Form(...),
    main_image: UploadFile = File(...),
    sub_images: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user: int = Depends(get_current_user),
):
    check_if_admin(user.id, db)
    if not check_if_category_exists(category, db):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Category not found")

    saved_main_image_path = save_image_to_file(main_image, category, name)
    saved_sub_images_paths = [
        save_image_to_file(sub_image, category, name, path_type="sub") for sub_image in sub_images
    ]

    product = Product(
        name=name,
        price=price,
        stock=stock,
        category=category,
        description=description,
        main_image=saved_main_image_path,
        sub_images=", ".join(saved_sub_images_paths) if saved_sub_images_paths else None,  # Store comma-separated paths
    )
    try:
        db.add(product)
        db.commit()

        db.refresh(product)
    
        return {"message": "Product created successfully", "product_id": product.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@product_router.get("/",status_code=status.HTTP_200_OK ,response_model=List[Products_Response])
def get_all_products(db: Session = Depends(get_db),Limit:int = 10,skip:int =0):
    products = db.query(Product).limit(Limit).offset(skip).all()
    return [{"id": product.id, "name": product.name, "price": product.price, "stock": product.stock, "category": product.category, "description": product.description, "main_image": send_file(product.main_image), "sub_images": [send_file(sub_image) for sub_image in product.sub_images.split(", ") if sub_image]} for product in products]

@product_router.get("/{product_id}", status_code=status.HTTP_200_OK,response_model=Products_Response)
def get_product_by_id_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"id": product.id, "name": product.name, "price": product.price, "stock": product.stock, "category": product.category, "description": product.description, "main_image": send_file(product.main_image), "sub_images": [send_file(sub_image) for sub_image in product.sub_images.split(", ") if sub_image]}

@product_router.patch("/{product_id}", response_model=Product_Response)
def update_product_by_id(product_id: int, product_update: Product_Update_Request, db: Session = Depends(get_db), user: int = Depends(get_current_user)):
    check_if_admin(user.id,db)
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if product_update.main_image:
        saved_main_image_path = save_image_to_file(product_update.main_image, product_update.category, product_update.name)
        product.main_image = saved_main_image_path
    if product_update.sub_images:
        saved_sub_images_paths = [save_image_to_file(sub_image, product_update.category, product_update.name, path_type="sub") for sub_image in product_update.sub_images]
        product.sub_images = ", ".join(saved_sub_images_paths) if saved_sub_images_paths else None
    
    if product_update.name:
        product.name = product_update.name
    if product_update.price:
        product.price = product_update.price
    if product_update.stock:
        product.stock = product_update.stock
    if product_update.category:
        product.category = product_update.category
    if product_update.description:
        product.description = product_update.description
    
    try:
        db.commit()
        db.refresh(product)
        return {"message": "Product updated successfully", "product_id": product.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))@product_router.delete("/{product_id}",status_code=status.HTTP_204_NO_CONTENT)

@product_router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_by_id(product_id: int,db: Session = Depends(get_db),user: int = Depends(get_current_user)):
    check_if_admin(user.id, db)
    product = get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    # Delete the main image file
    if os.path.isfile(product.main_image):
        os.remove(product.main_image)
    
    # Delete the sub-images files
    for sub_image in product.sub_images.split(", "):
        if sub_image and os.path.isfile(sub_image):
            os.remove(sub_image)
    
    # Delete the product directory
    product_dir = os.path.dirname(product.main_image)
    if os.path.isdir(product_dir):
        shutil.rmtree(product_dir)
    
    try:
        db.delete(product)
        db.commit()
        return {"message": "Product deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@product_router.delete('/',status_code=status.HTTP_204_NO_CONTENT)
def delete_all_products(db: Session = Depends(get_db),user: int = Depends(get_current_user),status_code=status.HTTP_204_NO_CONTENT):
    try:
        check_if_admin(user.id, db)
        products = db.query(Product).all()
        for product in products:
            # Delete the main image file
            if os.path.isfile(product.main_image):
                os.remove(product.main_image)
            
            # Delete the sub-images files
            for sub_image in product.sub_images.split(", "):
                if sub_image and os.path.isfile(sub_image):
                    os.remove(sub_image)
            
            # Delete the product directory
            product_dir = os.path.dirname(product.main_image)
            if os.path.isdir(product_dir):
                shutil.rmtree(product_dir)
        
        db.query(Product).delete()
        db.commit()
        return {"message": "All products deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

