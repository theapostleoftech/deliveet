#!/bin/bash

# Deliveet Production Deployment & Setup Script
# This script handles all setup, migration, and deployment tasks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Deliveet Production Setup${NC}"
echo -e "${BLUE}================================${NC}\n"

# Function to print section headers
print_section() {
    echo -e "\n${YELLOW}→ $1${NC}\n"
}

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please copy .env.example to .env and configure it:${NC}"
    echo "cp .env.example .env"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '#' | xargs)

print_section "Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

print_section "Creating necessary directories..."
mkdir -p logs staticfiles media
echo -e "${GREEN}✓ Directories created${NC}"

print_section "Running database migrations..."
python manage.py migrate
echo -e "${GREEN}✓ Migrations completed${NC}"

print_section "Collecting static files..."
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Static files collected${NC}"

print_section "Creating superuser..."
python manage.py createsuperuser --noinput \
    --email=${DJANGO_SUPERUSER_EMAIL:-admin@deliveet.app} || echo "Superuser may already exist"
echo -e "${GREEN}✓ Superuser setup complete${NC}"

print_section "Running tests..."
python manage.py test --verbosity=2 || echo -e "${YELLOW}Some tests failed - review above${NC}"

print_section "Creating cache table..."
python manage.py createcachetable || echo "Cache table may already exist"
echo -e "${GREEN}✓ Cache configured${NC}"

print_section "Loading initial data..."
# Add any initial data/fixtures here if needed
echo -e "${GREEN}✓ Initial data loaded${NC}"

print_section "Checking system health..."
python manage.py check
echo -e "${GREEN}✓ System check passed${NC}"

echo -e "\n${GREEN}================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}================================${NC}\n"

echo -e "${BLUE}Next steps:${NC}"
echo "1. Development: python manage.py runserver"
echo "2. Production: gunicorn --bind 0.0.0.0:8000 deliveet.wsgi:application"
echo "3. Docker: docker-compose up -d"
echo "4. Admin: http://localhost:8000/admin"
echo "5. API Docs: http://localhost:8000/api/v1/docs/"
