from pydantic import BaseModel, ConfigDict, EmailStr, constr
from typing import Optional

class UserCreate(BaseModel):
    name: constr(min_length=1)
    email: EmailStr

class UserUpdate(UserCreate):
    pass

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    title: constr(min_length=1)
    description: Optional[str] = ''
    status: Optional[constr(pattern='^(pending|done)$')] = 'pending'
    user_id: int

class TaskUpdate(TaskCreate):
    pass

class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    status: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)
