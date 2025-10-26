# Blog Panel

A full-stack blog management system for SEO teams to manage client websites' blog posts. Built with FastAPI backend and Next.js frontend.

## Features

- **Multi-client Support**: Manage blog posts for multiple client websites
- **Simple Authentication**: Easy login with fixed credentials (no complex user management)
- **Blog CRUD Operations**: Create, read, update, delete blog posts
- **Image Upload**: Upload and manage featured images for blog posts
- **Rich Content**: Ready for WYSIWYG editor integration
- **Search & Filtering**: Filter posts by client, status, and search content
- **Responsive Design**: Modern UI with Tailwind CSS and shadcn/ui components
- **Docker Support**: Complete containerized setup with docker-compose

## Tech Stack

| Layer | Technology | Description |
|-------|------------|-------------|
| **Backend** | FastAPI | REST API for blog management |
| **Database** | PostgreSQL | Main data store |
| **ORM** | SQLAlchemy + Alembic | Schema definition + migrations |
| **Auth** | Simple Email/Password | Basic authentication |
| **Frontend** | Next.js + TypeScript | Admin dashboard |
| **Styling** | Tailwind CSS | UI framework |
| **Deployment** | Docker Compose | Multi-service container setup |

## Quick Start

### Prerequisites

- Docker and Docker Compose

### Using Docker (Recommended)

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd blog-panel
   ```

2. **Start the Application**
   ```bash
   # On Windows
   setup.bat

   # On Linux/Mac
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Login Credentials**
   ```
   Email: admin@example.com
   Password: admin123
   ```

### Local Development

1. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env  # Configure environment variables
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.local.example .env.local  # Configure environment variables
   npm run dev
   ```

## Project Structure

```
blog-panel/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main FastAPI application
│   │   ├── models.py       # SQLAlchemy models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── database.py     # Database configuration
│   │   └── __init__.py
│   ├── alembic/            # Database migrations
│   ├── uploads/            # Uploaded images
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # Next.js app directory
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities and API clients
│   │   └── types/         # TypeScript type definitions
│   ├── package.json
│   ├── tailwind.config.js
│   ├── tsconfig.json
│   └── Dockerfile
├── uploads/                # Shared uploads directory
└── docker-compose.yml     # Docker orchestration
```

## API Endpoints

### Authentication
- `POST /login` - Simple login with email/password
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

## Authentication

The system uses simple authentication with fixed credentials:

**Default Login:**
- Email: `admin@example.com`
- Password: `admin123`

You can change these credentials in the environment variables:
- `ADMIN_EMAIL` - Admin email address
- `ADMIN_PASSWORD` - Admin password

## Environment Variables

### Backend (.env)
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

### Frontend (.env.local)
```env
# Backend API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Application Configuration
NEXT_PUBLIC_APP_NAME=Blog Panel
NEXT_PUBLIC_APP_VERSION=1.0.0
```

## Development

### Adding New Features

1. **Backend Changes**
   - Add models to `app/models.py`
   - Add schemas to `app/schemas.py`
   - Add routes to `app/main.py`
   - Create migration with `alembic revision -m "description"`
   - Run migration with `alembic upgrade head`

2. **Frontend Changes**
   - Add API functions to `src/lib/api.ts`
   - Add types to `src/types/api.ts`
   - Create components in `src/components/`
   - Add pages in `src/app/`

### Database Migrations

```bash
# Create new migration
alembic revision -m "Add new feature"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
