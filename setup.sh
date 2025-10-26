#!/bin/bash

# Blog Panel Setup Script

echo "🚀 Setting up Blog Panel..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Start the services
echo "📦 Starting services with docker-compose..."
docker-compose up -d

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 10

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose exec backend alembic upgrade head

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📱 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "🔐 Login credentials:"
echo "   Email: admin@example.com"
echo "   Password: admin123"
echo ""
echo "🛑 To stop the services:"
echo "   docker-compose down"
