from pydantic import BaseModel, Field

class Post(BaseModel):
    id: int
    title: str
    body: str
    userId: int

class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str
