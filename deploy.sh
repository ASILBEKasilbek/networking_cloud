#!/bin/bash
set -e

echo "========================================="
echo "  Wholesale Platform - Server Deployment"
echo "========================================="

# 1. Update system
echo "[1/7] Updating system packages..."
sudo apt-get update -y
sudo apt-get install -y docker.io docker-compose git curl

# 2. Start Docker
echo "[2/7] Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER

# 3. Clone or pull latest code
echo "[3/7] Setting up project..."
PROJECT_DIR="/home/ubuntu/networking_cloud/networking"

if [ -d "$PROJECT_DIR" ]; then
    echo "Project exists, pulling latest..."
    cd "$PROJECT_DIR"
    git pull origin main
else
    echo "Cloning project..."
    cd /home/ubuntu
    git clone https://github.com/ASILBEKasilbek/networking_cloud.git
    cd /home/ubuntu/networking_cloud/networking
fi

# 4. Setup .env file
echo "[4/7] Setting up environment..."
cd "$PROJECT_DIR"
if [ ! -f .env ]; then
    cp .env.production .env
    echo ">>> .env file created from .env.production"
    echo ">>> IMPORTANT: Edit .env and change SECRET_KEY and DATABASE_PASSWORD!"
fi

# 5. Create necessary directories
echo "[5/7] Creating directories..."
mkdir -p logs media staticfiles

# 6. Build and start containers
echo "[6/7] Building and starting Docker containers..."
sudo docker-compose down 2>/dev/null || true
sudo docker-compose up -d --build

# 7. Wait and check status
echo "[7/7] Checking deployment status..."
sleep 15
sudo docker-compose ps

echo ""
echo "========================================="
echo "  Deployment Complete! 🎉"
echo "========================================="
echo ""
echo "  Access URLs:"
echo "  - Admin:     http://admin.13.213.12.202/admin/"
echo "  - Dashboard: http://dashboard.13.213.12.202/"
echo "  - Portal:    http://portal.13.213.12.202/"
echo "  - API:       http://13.213.12.202/api/v1/"
echo "  - Health:    http://13.213.12.202/health/"
echo ""
echo "  Default login: admin / admin"
echo ""
echo "  Useful commands:"
echo "  - Logs:    sudo docker-compose logs -f"
echo "  - Status:  sudo docker-compose ps"
echo "  - Restart: sudo docker-compose restart"
echo "  - Stop:    sudo docker-compose down"
echo ""
