#!/usr/bin/env bash
# ==============================================================================
# Project: Cloud-Based Website Hosting and Monitoring System Using AWS
# Course: Fundamentals of Cloud Computing
# Script: deploy.sh - Automated EC2 Web Server Deployment Script (Apache)
# Target OS: Ubuntu 20.04 / 22.04 / 24.04 LTS on AWS EC2
# ==============================================================================

set -euo pipefail

# Visual color codes for clean terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}  AWS EC2 Deployment: Cloud-Based Hosting & Monitoring System    ${NC}"
echo -e "${BLUE}  Course: Fundamentals of Cloud Computing                       ${NC}"
echo -e "${BLUE}==================================================================${NC}"

# 1. Determine script directory and website folder location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WEBSITE_SRC="${SCRIPT_DIR}/website"
WEB_DEST="/var/www/html"

echo -e "\n${YELLOW}[Step 1/5] Verifying repository source files...${NC}"
if [ ! -d "${WEBSITE_SRC}" ]; then
  echo -e "${RED}[ERROR] Website directory not found at: ${WEBSITE_SRC}${NC}"
  echo -e "Please ensure you run this script from the root of the repository."
  exit 1
fi

if [ ! -f "${WEBSITE_SRC}/index.html" ]; then
  echo -e "${RED}[ERROR] index.html not found inside: ${WEBSITE_SRC}${NC}"
  exit 1
fi
echo -e "${GREEN}[OK] Website files verified at: ${WEBSITE_SRC}${NC}"

# 2. Update package cache and install Apache if not present
echo -e "\n${YELLOW}[Step 2/5] Checking and installing Apache HTTP Server (apache2)...${NC}"
sudo apt-get update -y

if ! command -v apache2 &> /dev/null; then
  echo -e "Apache is not installed. Installing apache2 via apt..."
  sudo apt-get install -y apache2
  echo -e "${GREEN}[OK] Apache successfully installed.${NC}"
else
  echo -e "${GREEN}[OK] Apache (apache2) is already installed.${NC}"
fi

# 3. Prepare web directory and deploy website files
echo -e "\n${YELLOW}[Step 3/5] Deploying website files to ${WEB_DEST}...${NC}"

# Backup default Ubuntu Apache welcome page if present
if [ -f "${WEB_DEST}/index.html" ] && [ ! -f "${WEB_DEST}/index.html.original_backup" ]; then
  echo -e "Backing up default Apache welcome page to index.html.original_backup..."
  sudo cp "${WEB_DEST}/index.html" "${WEB_DEST}/index.html.original_backup"
fi

# Clean destination html folder or copy over
sudo rm -rf "${WEB_DEST:?}"/*
sudo cp -r "${WEBSITE_SRC}/." "${WEB_DEST}/"

# Set optimal web server file ownership and read permissions
sudo chown -R www-data:www-data "${WEB_DEST}"
sudo chmod -R 755 "${WEB_DEST}"
echo -e "${GREEN}[OK] Files copied to ${WEB_DEST} with proper www-data permissions.${NC}"

# 4. Enable and restart Apache service
echo -e "\n${YELLOW}[Step 4/5] Enabling and restarting Apache service...${NC}"
sudo systemctl enable apache2
sudo systemctl restart apache2

# 5. Health verification
echo -e "\n${YELLOW}[Step 5/5] Verifying Apache service health...${NC}"
if systemctl is-active --quiet apache2; then
  echo -e "${GREEN}[SUCCESS] Apache HTTP Server is active and running!${NC}"
else
  echo -e "${RED}[ERROR] Apache failed to start. Inspect logs with: sudo journalctl -u apache2 -n 20${NC}"
  exit 1
fi

# Test local HTTP response
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/ || true)
if [ "${HTTP_CODE}" = "200" ]; then
  echo -e "${GREEN}[SUCCESS] Local HTTP request returned status 200 OK.${NC}"
else
  echo -e "${YELLOW}[WARN] Local HTTP check returned status: ${HTTP_CODE}.${NC}"
fi

# Attempt to discover public IP address
PUBLIC_IP=$(curl -s --connect-timeout 3 http://checkip.amazonaws.com 2>/dev/null || curl -s --connect-timeout 3 https://ifconfig.me 2>/dev/null || echo "")

echo -e "\n${BLUE}==================================================================${NC}"
echo -e "${GREEN}  DEPLOYMENT COMPLETE!                                            ${NC}"
echo -e "${BLUE}==================================================================${NC}"
if [ -n "${PUBLIC_IP}" ]; then
  echo -e "Your website is live at:"
  echo -e "  👉 ${GREEN}http://${PUBLIC_IP}/${NC}"
else
  echo -e "Your website is live! Open your browser and navigate to:"
  echo -e "  👉 ${GREEN}http://<YOUR_EC2_PUBLIC_IPV4>/${NC}"
fi
echo -e "\n${YELLOW}Note for Beginners:${NC}"
echo -e "1. Make sure your EC2 Security Group has an Inbound Rule for ${GREEN}HTTP (Port 80)${NC} from 0.0.0.0/0."
echo -e "2. Use ${GREEN}http://${NC} in your browser (not https://) since SSL is not configured yet."
echo -e "${BLUE}==================================================================${NC}\n"
