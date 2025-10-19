from pydantic import BaseModel
from app.models.user import User

class HashRequest(BaseModel):
    data: User
    hash_func: str

class HashResponse(BaseModel):
    hash: str
