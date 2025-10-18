from pydantic import BaseModel

class HashRequest(BaseModel):
    data: str
    hash_func: str

class HashResponse(BaseModel):
    hash: str
