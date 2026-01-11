from pydantic import BaseModel
from typing import Optional

class TermBase(BaseModel):
    name: str
    description: str
    link: Optional[str] = None

class TermCreate(TermBase):
    pass

class TermResponse(TermBase):
    id: int

    class Config:
        orm_mode = True
