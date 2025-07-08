#!/usr/bin/env bash
# build.sh - Render build script for CalorieTracker

set -o errexit  # exit on error

echo "Starting build process for CalorieTracker..."

# Install system dependencies for psycopg2
echo "Installing system dependencies for PostgreSQL..."
apt-get update
apt-get install -y libpq-dev gcc python3-dev

# Upgrade pip and install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if dataset.csv exists
echo "Checking for dataset.csv..."
if [ ! -f "dataset.csv" ]; then
    echo "❌ ERROR: dataset.csv not found in project root!"
    echo "Available files in current directory:"
    ls -la
    echo ""
    echo "Please ensure dataset.csv is committed to your repository"
    exit 1
fi

echo "✅ dataset.csv found ($(wc -l < dataset.csv) lines)"

# Set Django settings
export DJANGO_SETTINGS_MODULE=nutrition.production_settings

# Test database connection
echo "Testing database connection..."
python manage.py shell -c "
import django
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute('SELECT version();')
        version = cursor.fetchone()[0]
        print(f'✅ Database connection successful: {version[:50]}...')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Load food data with proper error handling
echo "Loading food data..."
python manage.py shell -c "
from calories.models import Food
import csv
import os

# Check if food data already exists
food_count = Food.objects.count()
print(f'Current food items in database: {food_count}')

if food_count == 0:
    print('No food data found, loading from CSV...')
    try:
        # Load data directly in shell to handle errors better
        csv_file_path = 'dataset.csv'
        foods_created = 0
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Extract calories from the string (remove 'cal' and convert to int)
                    calories_str = row['Calories'].replace(' cal', '').replace(',', '')
                    calories = int(calories_str)
                    
                    # Create food object
                    food, created = Food.objects.get_or_create(
                        name=row['Food'].strip(),
                        defaults={
                            'serving': row['Serving'].strip(),
                            'calories_per_serving': calories
                        }
                    )
                    
                    if created:
                        foods_created += 1
                        
                except (ValueError, KeyError) as e:
                    print(f'Skipped row for {row.get(\"Food\", \"Unknown\")}: {str(e)}')
                    continue
        
        print(f'✅ Successfully loaded {foods_created} food items')
        
    except Exception as e:
        print(f'❌ Error loading food data: {e}')
        import traceback
        traceback.print_exc()
        exit(1)
else:
    print('✅ Food data already exists, skipping load')
"

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth.models import User
import os

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'adminpass123')

if not User.objects.filter(username=username).exists():
    try:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f'✅ Superuser {username} created successfully')
    except Exception as e:
        print(f'❌ Error creating superuser: {e}')
else:
    print(f'✅ Superuser {username} already exists')
"

# Final verification
echo "Verifying setup..."
python manage.py shell -c "
from calories.models import Food
from django.contrib.auth.models import User

food_count = Food.objects.count()
user_count = User.objects.count()

print(f'📊 Final Stats:')
print(f'  - Food items: {food_count}')
print(f'  - Users: {user_count}')

if food_count > 0:
    print('✅ Food data loaded successfully')
    # Show sample of foods
    sample_foods = Food.objects.all()[:3]
    for food in sample_foods:
        print(f'    Sample: {food.name} - {food.calories_per_serving} cal')
else:
    print('❌ Warning: No food data found')

if user_count > 0:
    print('✅ Users exist')
else:
    print('❌ Warning: No users found')
"

echo "🎉 Build process completed successfully!"