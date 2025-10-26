# Blog Panel Backend

FastAPI backend for managing client blogs with PostgreSQL database.

## Features

- **Simple Authentication**: Uses fixed email/password credentials
- **Multi-client Support**: Manage blogs for multiple client websites
- **Blog CRUD Operations**: Create, read, update, delete blog posts
- **Image Upload**: Upload and manage featured images
- **Search & Filtering**: Filter posts by client, status, and content
- **RESTful API**: Well-documented API with automatic docs

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```env
# Database Configuration
DATABASE_URL=postgresql://blog_user:blog_password@localhost:5432/blog_panel

# Application Configuration
DEBUG=True
API_HOST=0.0.0.0
API_PORT=8000

# Upload Configuration
UPLOAD_DIR=../uploads
MAX_FILE_SIZE=10485760

# Simple Auth Configuration
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

## Authentication

The system uses simple authentication with fixed credentials:

- **Email**: admin@example.com
- **Password**: admin123

All API endpoints require authentication by passing email and password as form data.

## API Documentation

Access Swagger UI at: http://localhost:8000/docs
Access ReDoc at: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /login` - Login with email/password
- `GET /users/me` - Get current user info

### Clients
- `GET /clients/` - List all clients
- `GET /clients/{id}` - Get client by ID
- `POST /clients/` - Create new client

### Blog Posts
- `GET /blogs/` - List blog posts (with filtering)
- `GET /blogs/{id}` - Get blog post by ID
- `POST /blogs/` - Create new blog post
- `PUT /blogs/{id}` - Update blog post
- `DELETE /blogs/{id}` - Delete blog post

### File Upload
- `POST /upload/` - Upload image files

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string
- `DEBUG` - Enable debug mode (True/False)
- `API_HOST` - Server host (default: 0.0.0.0)
- `API_PORT` - Server port (default: 8000)
- `UPLOAD_DIR` - Directory for file uploads (default: ../uploads)
- `MAX_FILE_SIZE` - Maximum file size in bytes (default: 10485760)
- `ADMIN_EMAIL` - Admin email for authentication (default: admin@example.com)
- `ADMIN_PASSWORD` - Admin password for authentication (default: admin123)
