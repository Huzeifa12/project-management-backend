from fastapi import Depends, HTTPException,status
from sqlalchemy.exc import IntegrityError

from App import models
from App.schema import CreateAdminSchemaBase
from App.utils import password_hasher
from sqlalchemy.orm import Session

class AdminService:

    def check_if_user_already_exists(self,admin_details:CreateAdminSchemaBase,db:Session):
            get_user=db.query(models.User).filter(models.User.email==admin_details.email).first()
            print(get_user)
            if get_user :
                return True
            return False
            
            
    def create_admin(self,admin_details:CreateAdminSchemaBase,db:Session):
            if self.check_if_user_already_exists(admin_details,db)==True:
                return {"message":f"User with email of {admin_details.email} already exists"}
            admin_details.password= password_hasher(admin_details.password)
            new_user=models.User(**admin_details.model_dump())
            db.add(new_user)
            try:
                db.commit()
            except IntegrityError as e:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f" {e}")
            db.refresh(new_user)
            
            return new_user
    

    def check_if_user_already_exist_by_id(self,id:int,db:Session):
         user=db.query(models.User).filter(models.User.id==id)
         if not user.first():
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user of id {id} does not exist")
         return user
    
    def make_admin(self,id:int,db:Session):

        user=self.check_if_user_already_exist_by_id(id,db)
        if user.first().role=="admin":
             
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User of name {user.first().email} is already an admin")
        user.update({"role":"admin"},synchronize_session=False)
        db.commit()
        db.refresh(user.first())
        return user.first()
    
    def remove_admin(self,id:int,db:Session):
        user=self.check_if_user_already_exist_by_id(id,db)
        if user.first().role!="admin":
             
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User of name {user.first().email} is already not an admin")
        user.update({"role":"member"},synchronize_session=False)
        db.commit()
        db.refresh(user.first())
        return user.first()
            