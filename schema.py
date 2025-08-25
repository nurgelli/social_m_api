from pydantic import BaseModel, Field

class PostBase(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=150)
    published: bool | None = False
    
    
class PostCreate(PostBase):
    id: int = Field(ge=1)
    
class PostUpdate(BaseModel):
    title: str = Field(None, min_length=1, max_length=50)
    content: str | None

class PostOut(PostBase):
    id: int = Field(ge=1)