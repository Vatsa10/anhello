from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = "editor"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Client schemas
class ClientBase(BaseModel):
    name: str
    domain: str

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Blog post schemas
class BlogPostBase(BaseModel):
    title: str
    content: str
    tags: Optional[str] = None
    category: Optional[str] = None
    featured_image: Optional[str] = None
    meta_description: Optional[str] = None
    slug: str
    status: Optional[str] = "draft"

class BlogPostCreate(BlogPostBase):
    client_id: int

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None
    category: Optional[str] = None
    featured_image: Optional[str] = None
    meta_description: Optional[str] = None
    slug: Optional[str] = None
    status: Optional[str] = None

class BlogPost(BlogPostBase):
    id: int
    client_id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    client: Optional[Client] = None
    author: Optional[User] = None

    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str
