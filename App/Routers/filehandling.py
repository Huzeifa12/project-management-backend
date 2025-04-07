


from fastapi import APIRouter, Depends, Form, HTTPException,UploadFile,File,status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os,random
from App import models
from App.OAuth2 import get_current_user
from App.database import get_db
from App.schema import FileUploadSchema


router=APIRouter(
        prefix="/file",
        tags=["Files"]
)
digits="0123456789"
@router.post("/upload")
async def upload_file(receiver_id:int,id:int=Form(...),description:str=Form(...),file:UploadFile=File(...), db:Session=Depends(get_db),current_user:dict=Depends(get_current_user)):
    receiver=db.query(models.User).filter(models.User.id==receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id of {receiver_id} not found')
    # sender=db.query(models.User).filter(models.User.id==current_user.id).first()
    # if not sender:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id of {current_user.id} not found')
    print(file.content_type) 
    dir_path=os.path.abspath('uploads')
    os.makedirs(dir_path,exist_ok=True)
    num="".join(random.sample(digits,9))
    file_path=os.path.join(dir_path,f"{num}-{file.filename}")
    
    try:
        new_file=models.File(
            id=id,
            file_name=file.filename,
            file_path=file_path,
            sender_id=current_user.id,
            file_description=description,
            receiver_id=receiver_id,
            content_type=file.content_type
            )
      
        db.add(new_file)
        db.commit()
        with open(file_path,"wb") as f: 
            f.write(await file.read())
        db.refresh(new_file)
        return {"file_id":new_file.id, "file_name":new_file.file_name, "file_path":new_file.file_path}
    except Exception as e:
        return{"error":f"error is {e}"}
    



@router.get("/view_my_uploads")
async def view_sent_files(db:Session=Depends(get_db),current_user:dict=Depends(get_current_user)):
    uploads=[]

    my_files=db.query(models.File).filter(models.File.sender_id==current_user.id).all()
     
    if not my_files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user of id {current_user.id} has not sent any files yet")

    for file in my_files:
    
        uploads.append(file)

    return uploads



@router.get("/view_recieved_files")
async def view_recieved_files(db:Session=Depends(get_db),current_user:dict=Depends(get_current_user)):
    downloads=[]
    received_files=db.query(models.File).filter(models.File.receiver_id==current_user.id).all()
    if not received_files:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user of id {current_user.id} has not recieved any files yet")
    for file in received_files:
        downloads.append(file)
    return downloads
        





@router.get("/downloadfile")
async def download_file(id:int ,db:Session=Depends(get_db),current_user:dict=Depends(get_current_user)):
    
    file=db.query(models.File).filter(models.File.id==id).first()
    if not file:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"file does not exist")
    return FileResponse(path=file.file_path,filename=file.file_name,media_type=file.content_type)

    
        
@router.delete("/delete/{id}")
async def delete_file(id:int,db:Session=Depends(get_db),current_user:dict=Depends(get_current_user)):
    file=db.query(models.File).filter(models.File.id==id)
    print(current_user.role)
    if file.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"file does not exist")
    if file.first().sender_id!=current_user.id and current_user.role!="admin":
        print(f"aaaaa{current_user.role}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"You are not authorized")
    os.remove(file.first().file_path)
    file.delete(synchronize_session=False)
    db.commit()
    raise  HTTPException(status_code=status.HTTP_202_ACCEPTED, detail=f"File with id of {id} deleted succesfully")


