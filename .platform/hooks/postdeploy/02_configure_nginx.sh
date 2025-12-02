#!/bin/bash

# Add static location block to NGINX config if it doesn't exist
if ! grep -q "location /static" /etc/nginx/conf.d/elasticbeanstalk/00_application.conf; then
    # Insert static location block before the main location block
    sed -i '1i\
location /static {\
    alias /var/app/current/staticfiles;\
    expires 1y;\
    add_header Cache-Control "public, immutable";\
}\
' /etc/nginx/conf.d/elasticbeanstalk/00_application.conf
    
    # Reload NGINX
    systemctl reload nginx
    
    echo "$(date): NGINX static location block added" >> /var/log/static-nginx-config.log
else
    echo "$(date): NGINX static location block already exists" >> /var/log/static-nginx-config.log
fi