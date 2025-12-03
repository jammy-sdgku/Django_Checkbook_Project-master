#!/bin/bash

# Fix static path in all NGINX configs
for conf in /etc/nginx/conf.d/elasticbeanstalk/*.conf; do
    if grep -q "/var/app/current/static;" "$conf" 2>/dev/null; then
        sed -i 's|/var/app/current/static;|/var/app/current/staticfiles;|g' "$conf"
        echo "$(date): Fixed static path in $conf" >> /var/log/nginx-static-fix.log
    fi
done

systemctl reload nginx