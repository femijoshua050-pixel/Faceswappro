#!/bin/bash
# setup_web.sh - Script to install and setup the web version

# Update package index
sudo apt update

# Install necessary packages for web setup
sudo apt install -y nginx nodejs npm

# Setup Nginx configuration (example)
# sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup
# echo 'server {
    listen 80;
    server_name your_domain;
    location / {
        root /var/www/your_app;
        index index.html;
    }
}' | sudo tee /etc/nginx/sites-available/your_app

# Start and enable Nginx service
sudo systemctl start nginx
sudo systemctl enable nginx

# Install application dependencies
# cd /path/to/your/app
# npm install

echo 'Web setup completed.'