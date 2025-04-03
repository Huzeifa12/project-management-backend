from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class ProjectSchemaBase(BaseModel):

    id: int
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



class CreateUserSchemaBase(BaseModel):
    id: int
    first_name:str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str
    role:str="member"
    
    
class ViewProjectDetails(BaseModel):
    user_id:int
    project_details:ProjectResponse


class ProjectMemberDetails(BaseModel):
    member_details: UserDetailsForProject

class ViewProjectMembers(BaseModel):
    id:int
    member:ProjectMemberDetails