from typing import Optional
from fastapi import File, Form, UploadFile
from pydantic import BaseModel, EmailStr
from datetime import datetime

class ProjectSchemaBase(BaseModel):

    #id:int
    project_name:str
    description:str
    end_date:datetime
    
    

class ProjectUpdateSchemaBase(BaseModel):
    project_name:str
    description:str
    end_date: datetime


class CreateUserSchemaBase(BaseModel):
    id: int
    first_name:str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str

class CreateUserResponse(BaseModel):
    id: int
    first_name:str
    last_name: str
    email: EmailStr
    phone_number: str
# class UserResponse(BaseModel):

class ProjectResponseForTask(BaseModel):
    id:int
    project_name:str

class CreateUserSchemaBase(CreateUserSchemaBase):
    
    role:str="member"
class CreateAdminSchemaBase(CreateUserSchemaBase):
    role: str = "admin"

class UpdateUserSchemaBase(BaseModel):
    password:str
    

class UserDetailsForProject(BaseModel):
    first_name:str 
    last_name: str
    email: EmailStr
    role:str

class ProjectResponse(BaseModel):
    project_name:str
    description:str
    created_at:datetime
    end_date:datetime
    project_admin: int
    Owner: UserDetailsForProject
   




    
    
class ViewProjectDetails(BaseModel):
    user_id:int
    project_details:ProjectResponse


class ProjectMemberDetails(BaseModel):
    member_details: UserDetailsForProject

class ViewProjectMembers(BaseModel):
    id:int
    member:ProjectMemberDetails

class FileUploadSchema(BaseModel):

    id:int=Form(...)

class TaskSchemaBase(BaseModel):
    id: int
    
    assigned_to:int
    project_id:int
    title:str
    description:str
    assigned_at:datetime
    

class TaskResponse(TaskSchemaBase):
    sender_id:int  
    sender:CreateUserResponse
    receiver:CreateUserResponse
    project:ProjectResponseForTask

    