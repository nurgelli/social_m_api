from fastapi import FastAPI, Body, HTTPException, status
from pydantic import BaseModel, Field
from typing import Annotated, Dict
from schema import PostCreate, PostOut, PostUpdate



app = FastAPI()

_TODOS: Dict[int, "PostOut"] = {}

    
    
class PostRepo:
    
    @staticmethod
    def list_all_posts() -> list[PostOut]:
        return list(_TODOS.values())
    
    @staticmethod
    def get_post_by_id(post_id: int) -> PostOut:
        post = _TODOS.get(post_id)
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{post_id} not found")
        return post
    
    @staticmethod
    def add_post(data: PostCreate) -> PostOut:
        if data.id in _TODOS:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"{data.id} already exists")
        
        post = PostOut(**data.model_dump())
        _TODOS[data.id] = post
        return post
    
    @staticmethod
    def update_full_post(post_id: int, data: PostOut) -> PostOut:
        if post_id != data.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Path id must match Body id")
        if post_id not in _TODOS:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{post_id} not found")
        
        _TODOS[post_id] = data
        return data
    
    @staticmethod
    def update_partial_post(post_id: int, data: PostUpdate) -> PostOut:
        post = PostRepo.get_post_by_id(post_id)
        updated_post = post.model_copy(update={k: v for k, v in data.model_dump().items})
        _TODOS[post_id] = updated_post
        return data
        
    
    @staticmethod    
    def delete_post(post_id):
        if post_id not in _TODOS:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{post_id} not found")  
        del _TODOS[post_id]
        
@app.get("/posts", response_model=list[PostOut])
def get_posts():
    return PostRepo.list_all_posts()
        
@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int):
    return PostRepo.get_post_by_id(post_id)

@app.post("/posts/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def add_post(payload: PostCreate):
    return PostRepo.add_post(payload)

@app.put("/posts/{post_id}", response_model=PostOut)
def update_post(post_id: int, payload: PostOut):
    return PostRepo.update_full_post(post_id, payload)

@app.patch("/posts/{post_id}", response_model=PostOut)
def patch_post(post_id: int, payload: PostUpdate):
    return PostRepo.update_partial_post(post_id, payload)

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    return PostRepo.delete_post(post_id)
            
        
        

