from fastapi import APIRouter,Depends, HTTPException,status

from App import models
from App.OAuth2 import CheckRole, get_current_user
from ..schema import TaskSchemaBase,TaskResponse
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.exc import IntegrityError


router=APIRouter(
    prefix="/task",
    tags=["Task"]


)

admin_auth=CheckRole(["admin"])
@router.post("/",response_model=TaskResponse)
async def create_task(task_details:TaskSchemaBase, db:Session=Depends(get_db),current_user:dict=Depends(get_current_user),_:bool=Depends(admin_auth)):
    new_task=models.Task(sender_id=current_user.id,**task_details.model_dump())
    print(f'{task_details.model_dump()}')
    db.add(new_task)
    try:
        db.commit()
    except IntegrityError as e:
        
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unique key constraint violated{e}")
    
    db.refresh(new_task)
    return new_task

@router.get("/view-my-tasks",response_model=list[TaskResponse])
async def view_my_task(db:Session=Depends(get_db), current_user:dict=Depends(get_current_user)):
    print(current_user.id)
    my_task=db.query(models.Task).filter(models.Task.assigned_to==current_user.id).all()
    if not my_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No task for {current_user.email} found")

    return my_task
    
@router.get("/view-all-tasks",response_model=list[TaskResponse])
async def view_all_admin_assigned_task(db:Session=Depends(get_db), current_user:dict=Depends(get_current_user),_:bool=Depends(admin_auth)):
    print(current_user.id)
    my_task=db.query(models.Task).filter(models.Task.sender_id==current_user.id).all()
    if not my_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f" Admin {current_user.email} has not asaigned any task to anyone")
    

    return my_task
    
@router.get("/delete-task")
async def delete_task(id:int,db:Session=Depends(get_db),_:bool=Depends(admin_auth)):
    task=db.query(models.Task).filter(models.Task.id==id)
    if task.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"task with id of {id} not found")
    task.delete(synchronize_session=False)
    db.commit()
    raise  HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=f"task with id of {id} deleted succesfully")