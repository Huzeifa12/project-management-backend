from fastapi import Depends, FastAPI, Header,HTTPException,status
from typing import Optional
from pydantic import BaseModel
from sqlalchemy import text

from App.Routers import Auth, filehandling, user,admin,tasks
from .config import settings
from .database import  engine,Base,get_db
from . import models
from contextlib import asynccontextmanager
from .schema import ProjectSchemaBase, ProjectUpdateSchemaBase
from sqlalchemy.orm import Session
from .services import ProjectService
from .Routers import project
from .config import settings


@asynccontextmanager
async def booting(app:FastAPI):
    models.Base.metadata.create_all(bind=engine)
    print(f"Server has succesfully booteddd")
    print(settings.db_port)
    yield
    print('Server terminated')





app=FastAPI(
    lifespan=booting
)

app.include_router(project.router)
app.include_router(user.router)
app.include_router(Auth.router)
app.include_router(filehandling.router)
app.include_router(admin.router)
app.include_router(tasks.router)






#
#ProjectService=ProjectService()
# @app.post("/create_project",status_code=status.HTTP_201_CREATED)
# def create_project(projectinfo:ProjectSchemaBase,db:Session=Depends(get_db)):
#     create_project=ProjectService.createProject(projectinfo,db)
#     return create_project
    



# @app.get("/view_project")
# def view_project_by_id_search(db:Session=Depends(get_db),id:Optional[str]=None):

#     project= ProjectService.get_project(id,db)
#     if project==None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Project with id {id} doesn't exist")
        
#     return {status.HTTP_202_ACCEPTED, project.first()}
    

# @app.delete("/delete/{id}")
# def view_project_by_name_search(project_info:ProjectSchemaBase,id:str,db:Session=Depends(get_db)):
    
#     return ProjectService.delete_project(id,db)

# @app.patch("/update/{id}")
# def update_project(update_info:ProjectUpdateSchemaBase,id:str, db :Session=Depends(get_db)):
#     return ProjectService.update_project(update_info,id,db)



    
    
        
    




























@app.get("/")
async def firstPage():
    
    return{"message":f"hello Afo"}

# @app.get("/{name}")
# async def secondPage(name):
#     return {"message":f"my name is {name}"}

@app.get("/para/")
async def thirdPage(name:Optional[str]=None, age:int=11):
    if name: 
        return {"name": name, "age":age}
    return {"message":f"only age of {age } was provided"}

@app.get("/headers")
async def get_headers( Host: str =Header(None), User_Agent: str =Header(None), accept: str =Header(None)):
    request_header={}
    request_header["host"]=Host
    request_header["user-agent"]=User_Agent
    request_header["accept"]=accept
    return request_header

    pass
@app.get("/env")
async def read_env() -> dict:
    return {"name":settings.name}


       
# Check if the connection is active by pinging the database
# def check_connection():
#     try:
#         with engine.connect() as connection:
#             # Ping the connection to check if it's active
#             connection.execute(text("CREATE TABLE Gundem(id SERIAL PRIMARY KEY,name VARCHAR(255) NOT NULL,description TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);")) # Simple query
#             print("Database connection is active.")
#             return True
#     except Exception as e:
#         print(f"Database connection failed: {e}")
#         return False

# Test the connection

# print("Helooooo")
# check_connection()


