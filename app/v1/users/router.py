from fastapi.security.oauth2 import OAuth2PasswordRequestForm;
from fastapi import HTTPException,APIRouter,Depends,status;
from sqlalchemy.orm import Session;
from ...db.database import get_db;
from ...models.users import User;
from ...schemas.user import *;
from .OAuth2 import *;
from .utils import *;


user_router = APIRouter( tags = ['Users'] );

@user_router.post('/signup',status_code=status.HTTP_201_CREATED,response_model=User_Out)
def create_user(user:User_Create,db: Session = Depends(get_db)):  
    hashed_password = get_hashed_password(user.password);
    user.password = hashed_password;
    new_user = User(**user.model_dump());
    db.add(new_user);
    db.commit();
    db.refresh(new_user);
    return new_user;

@user_router.get('/',status_code=status.HTTP_200_OK,response_model=list[User_Out])
def get_all_users(db: Session = Depends(get_db),user: int = Depends(get_current_user)):
    check_if_admin(user.id,db)
    users = db.query(User).all();
    return users

@user_router.patch('/',status_code=status.HTTP_202_ACCEPTED,response_model=User_Out)
def update_user_password(user:Update_User,db:Session = Depends(get_db),current_user:int = Depends(get_current_user)):    
    fetched_user = db.query(User).filter(User.id == user.id).first();
    if not fetched_user: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist");
    if not verify_password(user.old_password,fetched_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials");
    hashed_new_password = get_hashed_password(user.new_password);
    fetched_user.password = hashed_new_password;
    db.add(fetched_user);
    db.commit();
    db.refresh(fetched_user);
    return fetched_user;

@user_router.post('/login',response_model=Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_credentials.username).first();
    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials");
    
    if not verify_password(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials");
    
    #generate access token
    access_token = generate_access_token(data = {'user_id':user.id})
    #return access token
    return {"token":access_token,"token_type":"Bearer"}