#!/usr/bin/env bash
# build.sh - Render build script for CalorieTracker

set -o errexit  # exit on error

echo "Starting build process for CalorieTracker..."

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Load food data if not already loaded
echo "Loading food data..."
python manage.py load_food_data || echo "Food data loading failed or already exists"

# Create superuser if it doesn't exist (optional)
echo "Creating superuser if needed..."
python manage.py shell << EOF
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully')
else:
    print(f'Superuser {username} already exists')
EOF

echo "Build process completed successfully!"