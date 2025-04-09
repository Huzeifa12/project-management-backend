from sqlalchemy import Column, DateTime, ForeignKey,String,Integer,Boolean, func
from .database import Base
from sqlalchemy.orm import relationship


class Project(Base):
    __tablename__='Project'

    id=Column(Integer, primary_key=True)
    project_name=Column(String, nullable=False)
    description=Column(String,nullable=False)
    created_at=Column(DateTime, server_default=func.now())
    end_date= Column(DateTime, nullable=False)
    project_admin=Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"))
    Owner=relationship("User")
    

    

class User(Base):
    __tablename__='Users'

    id=Column(Integer, primary_key=True)
    first_name=Column(String,nullable=False)
    last_name=Column(String,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    phone_number=Column(String,nullable=False,unique=True)
    created_at=Column(DateTime, server_default=func.now())
    role=Column(String,nullable=False)
    projects=relationship("ProjectMember", back_populates="member_details")

class ProjectMember(Base):
    __tablename__="ProjectMembers"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"))
    project_id=Column(Integer,ForeignKey("Project.id",ondelete="CASCADE"))
    member_details=relationship("User",back_populates="projects")
    project_details=relationship("Project")

class Task(Base):
    __tablename__="Tasks"
    id=Column(Integer,primary_key=True)
    sender_id=Column(Integer, ForeignKey("Users.id",ondelete="CASCADE"),nullable=False)
    assigned_to=Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"),nullable=False)
    project_id=Column(Integer,ForeignKey("Project.id",ondelete="CASCADE"),nullable=False)
    title=Column(String,nullable=False)
    description=Column(String,nullable=False)
    assigned_at=Column(DateTime,server_default=func.now())

    sender=relationship("User",foreign_keys=[sender_id])
    receiver=relationship("User", foreign_keys=[assigned_to])
    project=relationship("Project",foreign_keys=[project_id])


class File(Base):
    __tablename__="Files"
    id=Column(Integer,primary_key=True)
    file_name=Column(String,nullable=False)
    file_path=Column(String,nullable=False)
    content_type=Column(String)
    sender_id=Column(Integer, ForeignKey("Users.id",ondelete="CASCADE"))
    receiver_id=Column(Integer,ForeignKey("Users.id",ondelete="CASCADE"))
    uploaded_at=Column(DateTime,server_default=func.now())
    file_description=Column(String)
    

    sender=relationship('User',foreign_keys=[sender_id])
    receiver=relationship('User',foreign_keys=[receiver_id])