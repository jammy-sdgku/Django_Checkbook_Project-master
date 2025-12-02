#!/bin/bash

# Django Static Files Collection Script

# Exit on error
set -e

echo "Collecting static files for Django project..."

# Activate virtual environment
source /var/app/venv/*/bin/activate

# Navigate to application directory
cd /var/app/staging

# Collect static files
python manage.py collectstatic --noinput

echo "Django collectstatic completed"