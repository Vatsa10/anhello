@echo off
REM Blog Panel Setup Script for Windows

echo 🚀 Setting up Blog Panel...

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Start the services
echo 📦 Starting services with docker-compose...
docker-compose up -d

REM Wait for PostgreSQL to be ready
echo ⏳ Waiting for PostgreSQL to be ready...
timeout /t 10 /nobreak >nul

REM Run database migrations
echo 🗄️ Running database migrations...
docker-compose exec backend alembic upgrade head

echo.
echo 🎉 Setup complete!
echo.
echo 📱 Access the application:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 🔐 Login credentials:
echo    Email: admin@example.com
echo    Password: admin123
echo.
echo 🛑 To stop the services:
echo    docker-compose down
echo.
pause
