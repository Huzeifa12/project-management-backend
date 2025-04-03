from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    name:str
    db_password:str
    db_username:str
    db_hostname:str
    db_port:str
    db_name:str
    redis_host:str
    
    redis_port: str="6379"
    


    class Config:
        env_file=".env"

settings=Settings()