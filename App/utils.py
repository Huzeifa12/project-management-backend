from passlib.context import CryptContext


pwd_context=CryptContext(schemes=['bcrypt'],deprecated="auto")

def password_hasher(password:str):
    return pwd_context.hash(password)

def verifyPassword(plain_password, hashed_password):

    return pwd_context.verify(plain_password,hashed_password)