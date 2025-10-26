# Blog Panel Backend

FastAPI backend for managing client blogs with PostgreSQL database.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```env
DATABASE_URL=postgresql://blog_user:blog_password@localhost:5432/blog_panel
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000
UPLOAD_DIR=../uploads
MAX_FILE_SIZE=10485760
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Create initial admin user:
```python
# Run in Python shell with database connected
from app.models import User
from app.database import SessionLocal
from app.auth import get_password_hash

db = SessionLocal()
admin_user = User(
    username="admin",
    email="admin@example.com",
    hashed_password=get_password_hash("admin123"),
    role="admin"
)
db.add(admin_user)
db.commit()
```

5. Run the server:
```bash
uvicorn app.main:app --reload
```

## API Documentation

Access Swagger UI at: http://localhost:8000/docs
Access ReDoc at: http://localhost:8000/redoc

## Authentication

Use JWT tokens for authentication. Login via `/token` endpoint to get access token.

## Features

- User management with role-based access (admin/editor)
- Client management
- Blog post CRUD operations
- Image upload functionality
- Search and filtering
- JWT authentication
