#!/bin/bash
# This runs BEFORE EB tries to generate a Procfile
cd /var/app/staging
echo "web: gunicorn --bind 127.0.0.1:8000 --workers 3 --threads 2 --chdir Django_Checkbook Django_Checkbook.wsgi:application" > Procfile