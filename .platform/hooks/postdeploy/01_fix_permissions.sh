#!/bin/bash

# Fix static files permissions so NGINX can read them
chmod -R 755 /var/app/current/staticfiles/
chown -R webapp:webapp /var/app/current/staticfiles/

echo "Static files permissions fixed"