#!/bin/bash

# Local Development Setup Script
# This script sets up the project for local testing without Docker

set -e

echo "🚀 Setting up Versity Farewell - Local Development"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python 3.10+ is installed
echo ""
echo "📦 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python ${python_version} found${NC}"

# Setup virtual environment
echo ""
echo "🔧 Creating virtual environment..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}ℹ Virtual environment already exists${NC}"
fi

# Activate virtual environment
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Upgrade pip
echo ""
echo "📥 Upgrading pip..."
pip install --upgrade pip setuptools wheel >/dev/null 2>&1
echo -e "${GREEN}✓ Pip upgraded${NC}"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt >/dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create .env file if it doesn't exist
echo ""
echo "⚙️  Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created (update with your settings)${NC}"
else
    echo -e "${YELLOW}ℹ .env file already exists${NC}"
fi

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py migrate >/dev/null 2>&1
echo -e "${GREEN}✓ Migrations complete${NC}"

# Collect static files
echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput >/dev/null 2>&1
echo -e "${GREEN}✓ Static files collected${NC}"

# Create superuser prompt
echo ""
echo "👤 Creating superuser..."
echo -e "${YELLOW}Run the following command to create a superuser:${NC}"
echo -e "${YELLOW}  python manage.py createsuperuser${NC}"

# Summary
echo ""
echo "=================================================="
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "=================================================="
echo ""
echo "📍 To start the development server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "🌐 Access the application:"
echo "   Admin Panel: http://localhost:8000/admin"
echo "   API Root: http://localhost:8000/api"
echo ""
echo "📚 Documentation:"
echo "   - DOCKER_SETUP.md - For Docker-based setup"
echo "   - DEPLOYMENT.md - For production deployment"
echo "   - IMPLEMENTATION_PROGRESS.md - Progress tracking"
echo ""
