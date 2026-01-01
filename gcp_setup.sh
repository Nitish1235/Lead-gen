#!/bin/bash
# GCP VM Setup Script for B2B Lead Discovery System
# Run this script on a fresh Ubuntu VM instance

set -e  # Exit on error

echo "=========================================="
echo "B2B Lead Discovery - GCP VM Setup"
echo "=========================================="
echo ""

# Update system
echo "[1/7] Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip
echo "[2/7] Installing Python and pip..."
sudo apt install -y python3 python3-pip python3-venv git

# Install Chrome for Selenium
echo "[3/7] Installing Google Chrome..."
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt update
sudo apt install -y google-chrome-stable

# Install ChromeDriver dependencies
echo "[4/7] Installing ChromeDriver dependencies..."
sudo apt install -y unzip wget

# Install screen for background sessions
echo "[5/7] Installing screen utility..."
sudo apt install -y screen

# Create directory structure
echo "[6/7] Creating directory structure..."
mkdir -p ~/.config/lead-discovery
mkdir -p ~/lead-gen

# Install Python dependencies (if requirements.txt exists)
if [ -f "requirements.txt" ]; then
    echo "[7/7] Installing Python dependencies..."
    pip3 install --user -r requirements.txt
else
    echo "[7/7] Warning: requirements.txt not found. Install dependencies manually."
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Copy your credentials.json to ~/.config/lead-discovery/"
echo "2. Copy your application files to ~/lead-gen/"
echo "3. Create .env file in ~/lead-gen/ with your configuration"
echo "4. Run: cd ~/lead-gen && python3 main.py"
echo ""
echo "For long-running sessions, use screen:"
echo "  screen -S lead-discovery"
echo "  python3 main.py"
echo "  (Ctrl+A, then D to detach)"
echo "  screen -r lead-discovery (to reattach)"
echo ""

