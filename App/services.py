#this file contains utility functions for projects, user-management, and role handling


from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from App import models
from App.database import get_db
from App.schema import ProjectSchemaBase, ProjectUpdateSchemaBase,CreateUserSchemaBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from App.utils import password_hasher



class ProjectService:
    async def check_membership(self,project_id:int,user_id:int,db:Session):
        project=db.query(models.Project).filter(models.Project.id==project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id of {project_id} not found")

        user=db.query(models.User).filter(models.User.id==user_id).first()
        if not user:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id of {user_id} not found")
        
        existing_member=db.query(models.ProjectMember).filter(models.ProjectMember.user_id==user_id , models.ProjectMember.project_id==project_id ).first()
            
        if existing_member :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"user {user_id} is already a member")
        return [existing_member,user,project]




    async def createProject(self,projectinfo:ProjectSchemaBase,db:Session,owner:int):
        

            
        new_project=models.Project(project_admin=owner,**projectinfo.model_dump())   
        db.add(new_project)
        try:
            db.commit()
        
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unique key constraint violated")
        db.refresh(new_project)

        check_user_and_project_registered= await self.check_membership(new_project.id, owner,db)
        #automatically add project creator as member of project
        try:
            if check_user_and_project_registered :
                project_member=models.ProjectMember(project_id=new_project.id,user_id=owner)
                db.add(project_member)
                db.commit()
        except Exception as e:
            return {"message":f"Could not add Project owner as member{e}" }


        return new_project
        
    

    async def get_project(self, id:int,db:Session):
          
        project=db.query(models.Project).filter(models.Project.id==id)
          
        if not project.first():
            return None
        return project
    
    def delete_project(self, id:str,db:Session):
          
        project_to_delete=self.get_project(id,db)
        if  project_to_delete==None:
            
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=f"Project with id of {id} does not exist")
          
          
        project_to_delete.delete(synchronize_session=False)
        db.commit()
        raise  HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=f"Project with id of {id} deleted succesfully")
    
    async def update_project(self, update_info:ProjectUpdateSchemaBase,id:int, db:Session):
         

        project_to_update=await self.get_project(id,db)
        check_project_to_update=project_to_update.first()
        if check_project_to_update ==None:
            raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=f"Project of id number {id} does not exist")
         
       
        

        try: 
            project_to_update.update(update_info.model_dump(),synchronize_session=False)   
            db.commit()
            updated_project=project_to_update.first()
            return updated_project
            #return {"message":f"Project of id number {id} updated succesfully","updated Project":updated_project}

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail=f"{e}")
        




    async def add_user_to_project(self,project_id, user_id,db:Session):
        
        check_user_and_project_registered= await self.check_membership(project_id, user_id,db)
        if check_user_and_project_registered :
            project_member=models.ProjectMember(project_id=project_id,user_id=user_id)
            db.add(project_member)
            db.commit()
            return {"message":f"User {check_user_and_project_registered[1].first_name} added to project {check_user_and_project_registered[2].project_name}"} 
    
    async def delete_user_from_project(self,project_id,user_id,db:Session):
        project=db.query(models.Project).filter(models.Project.id==project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id of {project_id} not found")

        user=db.query(models.User).filter(models.User.id==user_id).first()
        if not user:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id of {user_id} not found")
        
        user_to_delete=db.query(models.ProjectMember).filter(models.ProjectMember.project_id==project_id,models.ProjectMember.user_id==user_id)
        if not user_to_delete.first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User of name {user.first_name} is not part of project{project.project_name}")
        user_to_delete.delete(synchronize_session=False)
        db.commit()

        return {"message":f"User : {user.first_name} removed from project : {project.project_name}"}



    

    async def view_member_project(self,user_id:int, db:Session):
       

        member_project=db.query(models.ProjectMember).filter(models.ProjectMember.user_id==user_id).all()
        if not member_project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"member not added to any project")
        
        return member_project
    
    async def view_project_members(self,project_id:int, db:Session):
        member_details_list=[]
        
        project=db.query(models.Project).filter(models.Project.id==project_id).first()
        if not project:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Project not found")
        project_members=db.query(models.ProjectMember).filter(models.ProjectMember.project_id==project_id).all()
        if not project_members:
            
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Project has n member")
        for member in project_members:
            id=member.user_id
            member_detail=db.query(models.User).filter(models.User.id==id).first()
            
            member_details_list.append(member_detail)

        return member_details_list
            







class UserService:
    def check_if_user_already_exists(self, user_details:CreateUserSchemaBase,db:Session):
        get_user=db.query(models.User).filter(models.User.email==user_details.email).first()
        print(get_user)
        if get_user :
            return True
        return False
        
        
    def create_user(self,user_details:CreateUserSchemaBase,db:Session):
        if self.check_if_user_already_exists(user_details,db)==True:
            return {"message":f"User with email of {user_details.email} already exists"}
        user_details.password= password_hasher(user_details.password)
        new_user=models.User(**user_details.model_dump())
        db.add(new_user)
        try:
            db.commit()
        except IntegrityError as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Damnn {e}")
        db.refresh(new_user)
        
        return new_user
    


    


    




         
          