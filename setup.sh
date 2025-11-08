#!/bin/bash

# Stealth Network Monitor - Quick Setup Script
# For Termux and Android environments

echo "🚀 Stealth Network Monitor - Quick Setup"
echo "========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in Termux
if [[ $PWD == *"/data/data/com.termux/files/"* ]]; then
    echo -e "${BLUE}📱 Detected Termux environment${NC}"
    IS_TERMUX=true
else
    echo -e "${YELLOW}⚠️  Not in Termux environment - some features may not work${NC}"
    IS_TERMUX=false
fi

# Check Python version
echo -e "${BLUE}🐍 Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Install required packages (Termux only)
if [ "$IS_TERMUX" = true ]; then
    echo -e "${BLUE}📦 Installing Termux packages...${NC}"
    pkg update -y
    pkg install -y python kivy netstat-nat git
fi

# Install Python dependencies
echo -e "${BLUE}📚 Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install kivy>=2.1.0
pip install kivymd>=1.1.1

# Create necessary directories
echo -e "${BLUE}📁 Creating directories...${NC}"
mkdir -p logs
mkdir -p data
mkdir -p exports
mkdir -p reports

# Make scripts executable
chmod +x stealth_network_spy_fixed.py
chmod +x main.py

echo ""
echo -e "${GREEN}✅ Setup completed successfully!${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Run the monitor: ${BLUE}python3 stealth_network_spy_fixed.py${NC}"
echo "2. Or launch GUI:    ${BLUE}python3 main.py${NC}"
echo "3. Build APK:        ${BLUE}pip install buildozer && buildozer android debug${NC}"
echo ""
echo -e "${GREEN}🎉 Stealth Network Monitor is ready to use!${NC}"
