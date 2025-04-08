from fastapi import APIRouter, Depends

from App.OAuth2 import CheckRole
from App.database import get_db
from App.schema import CreateAdminSchemaBase, CreateUserSchemaBase
from App.adminService import AdminService
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/admin",
    tags=["Admin Service"]
)

adminService=AdminService()
admin_auth=CheckRole(["admin"])
@router.post("/")
def create_admin(admin_detail:CreateAdminSchemaBase,db:Session=Depends(get_db)):

    return adminService.create_admin(admin_detail,db)

@router.put("/make-admin")
def make_admin(id:int,db:Session=Depends(get_db),_:bool=Depends(admin_auth)):
    return adminService.make_admin(id,db)

@router.put("/remove-admin")
def remove_admin(id:int,db:Session=Depends(get_db),_:bool=Depends(admin_auth)):
    return adminService.remove_admin(id,db)