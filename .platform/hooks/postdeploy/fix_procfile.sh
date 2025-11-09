#!/bin/bash
# This runs AFTER EB generates its Procfile
echo "web: gunicorn --bind 127.0.0.1:8000 --workers 3 --threads 2 --chdir Django_Checkbook Django_Checkbook.wsgi:application" > /var/app/current/Procfile

# Restart the web service to pick up the new Procfile
systemctl restart web.service