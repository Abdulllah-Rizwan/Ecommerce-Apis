from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,status,HTTPException
from datetime import datetime,timedelta
from jose import JWTError,jwt
from ...settings import setting
from ...schemas.user import *;
from sqlalchemy.orm import Session;
from ...db.database import get_db
from ...models.users import User;

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = setting.SECRET_KEY;
ALGORITHM = setting.ALGORITHM;
ACCESS_TOKEN_EXPIRE_MIN = setting.ACCESS_TOKEN_EXPIRE_MINUTES;


def generate_access_token(data: dict):
    to_encode = data.copy();
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN) 
    to_encode.update({"exp":expiry});
    encoded_token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM);
    
    return encoded_token;

def varify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]);
        id:str = payload.get('user_id');
        if not id:
            raise credentials_exception;
        token_data = Token_Data(id=str(id));
    
    except JWTError:
        raise credentials_exception;    
    
   
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate":"Bearer"});
     token = varify_access_token(token,credentials_exception);
     user = db.query(User).filter(User.id == token.id).first();
     
     return user;