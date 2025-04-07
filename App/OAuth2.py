


from datetime import datetime
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer

from fastapi import Depends, HTTPException, status
import jwt

from App import models
from App.database import get_db
from sqlalchemy.orm import Session
from App.models import User
from App.config import settings

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/login/")

async def create_access_token(data:dict):
    pay_load=data.copy()
    time_to_expire=datetime.utcnow()+ timedelta(settings.access_token_expire_minutes)
    pay_load["exp"]=time_to_expire
    
    
    token=jwt.encode(pay_load,settings.secret_key,settings.algorithm )
    return token

def get_current_user(token: str=Depends(oauth2_scheme), db: Session=Depends(get_db)):
    payload=jwt.decode(token,settings.secret_key,settings.algorithm)

    current_user_id=payload["id"]
    if not current_user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Could not Validate token", headers={"WWW-Authenticate":"Bearer"})
    current_user_profile=db.query(models.User).filter(models.User.id==current_user_id).first()
    print(current_user_profile.id,"ooo")
    return current_user_profile



class CheckRole:
    def __init__(self, Allowed_roles:list):
        self.Allowed_roles=Allowed_roles

    def __call__(self, current_user:User=Depends(get_current_user)):
        
        if current_user.role in self.Allowed_roles:
            
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You do not have Permission")
        


  


    