

from fastapi import APIRouter, Depends

from App.database import get_db
from App.schema import CreateUserSchemaBase
from App.services import UserService
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/users",
    tags=["Users"]
)

userService=UserService()

@router.post("/")
def create_user(user_detail:CreateUserSchemaBase,db:Session=Depends(get_db)):
    
    return userService.create_user(user_detail,db)