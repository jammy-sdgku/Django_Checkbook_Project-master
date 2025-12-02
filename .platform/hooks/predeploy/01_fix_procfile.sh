#!/bin/bash

# Ensure the correct Procfile is used
echo "web: gunicorn --bind :8000 --workers 3 --threads 2 Django_Checkbook.wsgi:application" > /var/app/staging/Procfile

# Set proper permissions
chmod 644 /var/app/staging/Procfile

echo "Procfile has been fixed"