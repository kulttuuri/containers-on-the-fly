#!/bin/bash

##########################################################################################
### This script installs all requirements for the web servers to work on this machine. ### 
##########################################################################################

GREEN='\033[0;32m'
RED='\033[0;31m'
RESET='\033[0m'

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}This script must be run with sudo privileges.${RESET}"
    exit 1
fi

echo "Running with sudo privileges."

# Update and install initial packages
# TODO: Put back later when everything else is ready.
#sudo apt update

# Function to check if Nginx is installed
check_nginx_installed() {
    if dpkg -l | grep -q nginx; then
        echo "Nginx is already installed."
        return 0
    else
        echo "Nginx is not installed."
        return 1
    fi
}

# Function to install Nginx
install_nginx() {
    echo "Updating package list..."
    
    echo "Installing Nginx..."
    apt install -y nginx

    if [ $? -eq 0 ]; then
        echo "Nginx installed successfully."
    else
        echo -e "${RED}Failed to install Nginx.${RESET}"
        exit 1
    fi
}

# Check if Nginx is installed
check_nginx_installed
if [ $? -ne 0 ]; then
    install_nginx
fi

CURRENT_DIR=$(pwd)
CUSTOM_CONF="$CURRENT_DIR/user_config/nginx_settings.conf"

# Add custom configuration to nginx.conf if not already present
NGINX_CONF="/etc/nginx/nginx.conf"
if ! grep -q "include $CUSTOM_CONF;" $NGINX_CONF; then
    echo "Adding custom configuration to Nginx main configuration..."
    sudo sed -i "/http {/a \\    include $CUSTOM_CONF;" $NGINX_CONF
else
    echo -e "${GREEN}Custom configuration is already included in Nginx main configuration.${RESET}"
fi

# Disable the default site
if [ -L /etc/nginx/sites-enabled/default ]; then
    sudo rm /etc/nginx/sites-enabled/default
    echo -e "${GREEN}Default nginx site configuration disabled.${RESET}"
fi

# Test and reload Nginx
nginx -t
if [ $? -eq 0 ]; then
    systemctl reload nginx
    echo -e "${GREEN}Nginx configuration seems to be fine.${RESET}"
else
    echo -e "${RED}Nginx configuration test failed. Please check the configuration.${RESET}"
    exit 1
fi

# Ensure Nginx starts on boot and start Nginx
systemctl enable nginx
systemctl start nginx
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Nginx is now running and enabled to start on boot.${RESET}"
else
    echo -e "${RED}Failed to start Nginx.${RESET}"
    exit 1
fi

# Check if Nginx is active and enabled
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}Nginx is active.${RESET}"
else
    echo -e "${RED}Nginx is not running.${RESET}"
fi

if systemctl is-enabled --quiet nginx; then
    echo -e "${GREEN}Nginx is enabled to start on boot.${RESET}"
else
    echo -e "${RED}Nginx is not enabled to start on boot.${RESET}"
fi

# TODO: MARIADB
