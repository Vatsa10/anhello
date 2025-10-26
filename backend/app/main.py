from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import shutil
from datetime import timedelta
from typing import List, Optional

from app.database import get_db, engine
from app.models import Base, User, Client, BlogPost
from app.schemas import (
    UserCreate, User, ClientCreate, Client, BlogPostCreate, BlogPostUpdate,
    BlogPost, UserLogin, Token
)
from app.auth import (
    verify_password, get_password_hash, create_access_token,
    verify_token, ACCESS_TOKEN_EXPIRE_MINUTES
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependencies
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = verify_token(token, credentials_exception)
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# Routes

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# User routes
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Client routes
@app.post("/clients/", response_model=Client)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.domain == client.domain).first()
    if db_client:
        raise HTTPException(status_code=400, detail="Domain already registered")

    db_client = Client(name=client.name, domain=client.domain)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.get("/clients/", response_model=List[Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = db.query(Client).offset(skip).limit(limit).all()
    return clients

@app.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

# Blog routes
@app.post("/blogs/", response_model=BlogPost)
def create_blog_post(
    blog_post: BlogPostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if slug already exists
    db_blog = db.query(BlogPost).filter(BlogPost.slug == blog_post.slug).first()
    if db_blog:
        raise HTTPException(status_code=400, detail="Slug already exists")

    db_blog_post = BlogPost(
        **blog_post.dict(),
        author_id=current_user.id
    )
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post

@app.get("/blogs/", response_model=List[BlogPost])
def read_blog_posts(
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
def read_blog_post(blog_id: int, db: Session = Depends(get_db)):
    db_blog_post = db.query(BlogPost).filter(BlogPost.id == blog_id).first()
    if db_blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_blog_post

@app.put("/blogs/{blog_id}", response_model=BlogPost)
def update_blog_post(
    blog_id: int,
    blog_post_update: BlogPostUpdate,
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user),
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
    current_user: User = Depends(get_current_user)
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
