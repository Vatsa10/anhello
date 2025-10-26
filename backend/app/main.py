from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import shutil
from datetime import datetime
from typing import List, Optional

from app.database import get_db, engine
from app.models import Base, User, Client, BlogPost
from app.schemas import (
    UserCreate, User, ClientCreate, Client, BlogPostCreate, BlogPostUpdate,
    BlogPost, SimpleLogin
)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog Panel API",
    description="REST API for managing client blogs",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple authentication function
def verify_credentials(email: str, password: str) -> bool:
    """Simple authentication against environment variables"""
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    return email == admin_email and password == admin_password

# Dependencies
async def get_current_user(email: str = Form(...), password: str = Form(...)):
    """Simple authentication dependency"""
    if not verify_credentials(email, password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    return {"email": email, "authenticated": True}

# Routes

@app.post("/login")
async def login(credentials: SimpleLogin):
    """Simple login endpoint"""
    if verify_credentials(credentials.email, credentials.password):
        return {
            "message": "Login successful",
            "email": credentials.email,
            "authenticated": True
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

# User routes
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # For simple auth, we'll store password as plain text (not recommended for production)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password,  # Storing as plain text for simplicity
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    # In a real app, you'd fetch the user from database
    # For now, return a mock user
    return User(
        id=1,
        username="admin",
        email=current_user["email"],
        role="admin",
        is_active=True,
        created_at=datetime.now()
    )

# Client routes
@app.post("/clients/", response_model=Client)
def create_client(client: ClientCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.domain == client.domain).first()
    if db_client:
        raise HTTPException(status_code=400, detail="Domain already registered")

    db_client = Client(name=client.name, domain=client.domain)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients/", response_model=List[Client])
def read_clients(current_user: dict = Depends(get_current_user), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = db.query(Client).offset(skip).limit(limit).all()
    return clients

@app.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

# Blog routes
@app.post("/blogs/", response_model=BlogPost)
def create_blog_post(
    blog_post: BlogPostCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if slug already exists
    db_blog = db.query(BlogPost).filter(BlogPost.slug == blog_post.slug).first()
    if db_blog:
        raise HTTPException(status_code=400, detail="Slug already exists")

    # Create a mock author for simplicity (in real app, you'd get from current_user)
    author = db.query(User).filter(User.role == "admin").first()
    if not author:
        author = User(
            username="admin",
            email="admin@example.com",
            hashed_password="admin123",
            role="admin"
        )
        db.add(author)
        db.commit()
        db.refresh(author)

    db_blog_post = BlogPost(
        **blog_post.dict(),
        author_id=author.id
    )
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post

@app.get("/blogs/", response_model=List[BlogPost])
def read_blog_posts(
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    client_id: Optional[int] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(BlogPost)

    if client_id:
        query = query.filter(BlogPost.client_id == client_id)
    if status:
        query = query.filter(BlogPost.status == status)
    if search:
        query = query.filter(
            (BlogPost.title.contains(search)) |
            (BlogPost.content.contains(search)) |
            (BlogPost.tags.contains(search))
        )

    blog_posts = query.offset(skip).limit(limit).all()
    return blog_posts

@app.get("/blogs/{blog_id}", response_model=BlogPost)
def read_blog_post(blog_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    db_blog_post = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if db_blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_blog_post

@app.put("/blogs/{blog_id}", response_model=BlogPost)
def update_blog_post(
    blog_id: int,
    blog_post_update: BlogPostUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_blog_post = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if db_blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")

    update_data = blog_post_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_blog_post, field, value)

    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post

@app.delete("/blogs/{blog_id}")
def delete_blog_post(
    blog_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_blog_post = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if db_blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")

    db.delete(db_blog_post)
    db.commit()
    return {"message": "Blog post deleted successfully"}

# Image upload route
@app.post("/upload/")
async def upload_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="File type not allowed")

    # Validate file size (10MB max)
    max_size = int(os.getenv("MAX_FILE_SIZE", "10485760"))
    if file.size > max_size:
        raise HTTPException(status_code=400, detail="File too large")

    # Create uploads directory if it doesn't exist
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
    file_path = os.path.join(upload_dir, filename)

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": filename,
        "url": f"/uploads/{filename}",
        "message": "Image uploaded successfully"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
