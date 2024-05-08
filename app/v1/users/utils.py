from fastapi import HTTPException, status;
from passlib.context import CryptContext;
from ...models.users import User;

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto");

def check_if_admin(user_id:int,db):
    user = db.query(User).get(user_id);
    admin = user.is_admin;
    if not admin: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not an admin");
    
    
def get_hashed_password(password):
    return pwd_context.hash(password);

def verify_password(password,hashed_password):
    return pwd_context.verify(password,hashed_password);