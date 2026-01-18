#!/bin/bash

# Production deployment script
# Run this to deploy the application to production

set -e

echo "🚀 Starting Deliveet Production Deployment..."

# Load environment
export $(cat .env | grep -v '#' | xargs)

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down || true

# Build images
echo "Building Docker images..."
docker-compose build

# Start services
echo "Starting services..."
docker-compose up -d

# Wait for database to be ready
echo "Waiting for database..."
sleep 10

# Run migrations
echo "Running migrations..."
docker-compose exec -T web python manage.py migrate

# Collect static files
echo "Collecting static files..."
docker-compose exec -T web python manage.py collectstatic --noinput

# Create superuser
echo "Creating superuser..."
docker-compose exec -T web python manage.py createsuperuser --noinput || true

echo "✅ Deployment complete!"
echo ""
echo "Services running:"
echo "  - Web: http://localhost:8000"
echo "  - FastAPI: http://localhost:8001"
echo "  - API Docs: http://localhost:8000/api/v1/docs/"
echo ""
echo "To view logs: docker-compose logs -f"
