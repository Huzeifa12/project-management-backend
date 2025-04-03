from fastapi import Depends,APIRouter, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from App import OAuth2, models, utils
from App.database import get_db
from App.OAuth2 import get_current_user
from ..schema import CreateUserSchemaBase
from App.OAuth2 import CheckRole

router=APIRouter(
        prefix="/login",
        tags=["Authorization"]
)

admin_auth=CheckRole(["admin"])

@router.post("/")
async def login_user(login_info:OAuth2PasswordRequestForm=Depends(),db:Session= Depends(get_db)):
        
        user=db.query(models.User).filter(models.User.email==login_info.username).first()
        

        if  not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail=f"User with with email of {login_info.username} not found")
        
        if utils.verifyPassword(login_info.password,user.password)==False:
              raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")
        
        access_token=await OAuth2.create_access_token({"id":user.id,"role":user.role})
        

        return{"access_token":access_token, "token_type":"bearer"}
        
  
@router.get("/get_user" )
def get_profile(user:dict=Depends(get_current_user),_:bool=Depends(admin_auth)):
     
      return user.id
