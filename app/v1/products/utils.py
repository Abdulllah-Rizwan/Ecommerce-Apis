from ...models.category import Category;
from fastapi import UploadFile;
from...models.category import Category;
from ...models.products import Product;
from ...schemas.products import *
from sqlalchemy.orm import Session
from typing import List  
import os

def create_directory(path):
  """Creates a directory if it doesn't exist."""
  if not os.path.exists(path):
    os.makedirs(path)

def get_unique_filename(filename):
  """Generates a unique filename to avoid conflicts."""
  base, ext = os.path.splitext(filename)
  i = 1
  while os.path.exists(f"{base}_{i}{ext}"):
    i += 1
  return f"{base}_{i}{ext}"

def save_image_to_file(image: UploadFile, category: str, name: str, path_type: str = "main"):
  """Saves an uploaded image to a file with category and product name folders."""
  # Create category and product name folders
  category_path = os.path.join("images", category)
  create_directory(category_path)
  product_path = os.path.join(category_path, name.replace(" ", "_"))  # Replace spaces with underscores
  create_directory(product_path)

  # Generate a unique filename
  filename = get_unique_filename(image.filename)

  # Save the image to the specified path
  image_path = os.path.join(product_path, filename)
  with open(image_path, "wb") as buffer:
    buffer.write(image.file.read())
    
  # Return the complete path based on type (main or sub)
  if path_type == "main":
    return image_path
  else:
    return os.path.relpath(image_path, os.path.join("images", category))  # Return relative path for sub-images
  

def find_product_by_id_and_update(product_id, field_to_update: str, value_to_update_with, db: Session):
    product = db.query(Product).get(product_id)
    if not product:
        raise Exception("Product not found")
    setattr(product, field_to_update, value_to_update_with)
    try:
        db.commit()
        db.refresh(product)
        return product
    except Exception as e:
        db.rollback()
        raise Exception(status_code=500, detail=f"Error occurred when updating the product: {e}") 
  
def send_file(path: str):
    return {"filename": os.path.basename(path), "url": f"/images/{path}"}  
  
     

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def check_if_category_exists(category_name: int, db):
    return db.query(Category).filter(category_name == Category.name) is not None
