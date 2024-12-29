from pydantic import BaseModel

class TermBase(BaseModel):
    name: str
    description: str

class TermCreate(TermBase):
    pass

class TermResponse(TermBase):
    id: int

    class Config:
        orm_mode = True
