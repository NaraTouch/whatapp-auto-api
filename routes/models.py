from pydantic import BaseModel

class User(BaseModel):
    id: int
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: str
    password: str