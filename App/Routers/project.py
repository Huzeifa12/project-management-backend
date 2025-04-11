from typing import Optional
from fastapi import APIRouter, Depends,status,HTTPException

from App.OAuth2 import CheckRole, get_current_user
from App.database import get_db
from App.schema import ProjectSchemaBase,ProjectUpdateSchemaBase,ProjectResponse,ViewProjectDetails,UserDetailsForProject
from ..services import ProjectService
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/project",
    tags=["Project"]
)

ProjectService=ProjectService()
admin_auth=CheckRole(["admin"])

@router.post("/create-project",status_code=status.HTTP_201_CREATED,response_model=ProjectResponse)
async def create_project(projectinfo:ProjectSchemaBase,db:Session=Depends(get_db),user: dict=Depends(get_current_user),_:bool=Depends(admin_auth)):
    create_project=await ProjectService.createProject(projectinfo,db,user.id)
    return create_project
    

@router.get("/view-all-projects",response_model=list[ProjectResponse])
async def view_all_projects(db:Session=Depends(get_db),_:bool=Depends(admin_auth)):
    return await ProjectService.view_all_projects(db)

@router.get("/view-project",response_model=ProjectResponse)
async def view_project_by_id_search(db:Session=Depends(get_db),id:Optional[int]=None,user:dict=Depends(get_current_user)):

    project=await ProjectService.get_project(id,db)
    if project==None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Project with id {id} doesn't exist")
        
    project=project.first()
    return project
    

@router.put("/update_project/{id}",response_model=ProjectResponse)
async def update_project(update_info:ProjectUpdateSchemaBase,id: int,db:Session=Depends(get_db),current_user:dict=Depends(get_current_user),_:bool=Depends(admin_auth)):
    update_project= await ProjectService.update_project(update_info,id,current_user,db)
    return update_project
    


@router.delete("/delete/{id}")
async def delete_project_by_id(id:int,db:Session=Depends(get_db),user:dict=Depends(get_current_user),_:bool=Depends(admin_auth)):
    
    return await ProjectService.delete_project(id,db,user)


@router.post("/{project_id}/add-member/{user_id}")
async def add_member(project_id:int,user_id:int,db:Session=Depends(get_db),_:bool=Depends(admin_auth)):
    return await ProjectService.add_user_to_project(project_id,user_id,db)


@router.get("/{project_id}/get_members",response_model=list[UserDetailsForProject])
async def get_project_members(project_id:int,db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    return await ProjectService.view_project_members(project_id,db)

@router.get("/view-my-projects/",response_model=list[ViewProjectDetails])
async def view_my_projects(db:Session=Depends(get_db),user:dict=Depends(get_current_user)):
    return await ProjectService.view_member_project(user.id,db)

@router.delete("/{project_id}/delete-member/{user_id}")
async def remove_member_from_project(project_id:int,user_id:int, db:Session=Depends(get_db),current_user:dict=Depends(get_current_user),_:bool=Depends(admin_auth)):
    return await ProjectService.delete_user_from_project(project_id,user_id,current_user,db)
                                 