#!/usr/bin/env python3
"""
CalorieTracker Deployment Configuration Script
This script helps prepare the application for different deployment environments.
"""

import os
import sys
import subprocess
from pathlib import Path

class DeploymentConfig:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent
        self.project_name = "nutrition"
        
    def check_requirements(self):
        """Check if all requirements are installed"""
        print("🔍 Checking requirements...")
        
        try:
            import django
            print(f"✅ Django version: {django.get_version()}")
        except ImportError:
            print("❌ Django not installed")
            return False
            
        try:
            from PIL import Image
            print("✅ Pillow installed")
        except ImportError:
            print("❌ Pillow not installed")
            return False
            
        return True
    
    def setup_database(self):
        """Set up the database with migrations"""
        print("\n📚 Setting up database...")
        
        commands = [
            ["python", "manage.py", "makemigrations"],
            ["python", "manage.py", "migrate"],
        ]
        
        for cmd in commands:
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=self.base_dir)
            if result.returncode != 0:
                print(f"❌ Command failed: {' '.join(cmd)}")
                return False
                
        print("✅ Database setup complete")
        return True
    
    def load_food_data(self):
        """Load food data from CSV"""
        print("\n🍎 Loading food data...")
        
        result = subprocess.run(
            ["python", "manage.py", "load_food_data"],
            cwd=self.base_dir
        )
        
        if result.returncode == 0:
            print("✅ Food data loaded successfully")
            return True
        else:
            print("❌ Failed to load food data")
            return False
    
    def collect_static(self):
        """Collect static files for production"""
        print("\n📁 Collecting static files...")
        
        result = subprocess.run(
            ["python", "manage.py", "collectstatic", "--noinput"],
            cwd=self.base_dir
        )
        
        if result.returncode == 0:
            print("✅ Static files collected")
            return True
        else:
            print("❌ Failed to collect static files")
            return False
    
    def create_superuser(self):
        """Create superuser interactively"""
        print("\n👤 Creating superuser...")
        print("Please enter superuser details:")
        
        result = subprocess.run(
            ["python", "manage.py", "createsuperuser"],
            cwd=self.base_dir
        )
        
        return result.returncode == 0
    
    def setup_test_data(self):
        """Set up test data"""
        print("\n🧪 Setting up test data...")
        
        result = subprocess.run(
            ["python", "manage.py", "setup_test_data", "--create-user", "--create-entries"],
            cwd=self.base_dir
        )
        
        if result.returncode == 0:
            print("✅ Test data created")
            return True
        else:
            print("❌ Failed to create test data")
            return False
    
    def generate_secret_key(self):
        """Generate a new secret key for production"""
        from django.core.management.utils import get_random_secret_key
        return get_random_secret_key()
    
    def create_production_settings(self):
        """Create production settings file"""
        print("\n⚙️ Creating production settings...")
        
        secret_key = self.generate_secret_key()
        
        production_settings = f'''
"""
Production settings for CalorieTracker
"""
from .settings import *

DEBUG = False

ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']

SECRET_KEY = '{secret_key}'

# Database for production (PostgreSQL example)
# DATABASES = {{
#     'default': {{
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'calorietracker_db',
#         'USER': 'your_db_user',
#         'PASSWORD': 'your_db_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }}
# }}

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files for production
STATIC_ROOT = '/var/www/calorietracker/static/'
MEDIA_ROOT = '/var/www/calorietracker/media/'

# Logging
LOGGING = {{
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {{
        'file': {{
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/calorietracker/error.log',
        }},
    }},
    'loggers': {{
        'django': {{
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        }},
    }},
}}
'''
        
        settings_file = self.base_dir / "nutrition" / "production_settings.py"
        with open(settings_file, 'w') as f:
            f.write(production_settings)
            
        print(f"✅ Production settings created: {settings_file}")
        print(f"🔑 New secret key generated")
        
    def create_deployment_files(self):
        """Create deployment-specific files"""
        print("\n📄 Creating deployment files...")
        
        # requirements.txt (if not exists)
        requirements_file = self.base_dir / "requirements.txt"
        if not requirements_file.exists():
            requirements_content = """Django==5.2.4
Pillow==10.0.1
"""
            with open(requirements_file, 'w') as f:
                f.write(requirements_content)
            print("✅ requirements.txt created")
        
        # Procfile for Heroku
        procfile = self.base_dir / "Procfile"
        with open(procfile, 'w') as f:
            f.write("web: gunicorn nutrition.wsgi\n")
        print("✅ Procfile created (Heroku)")
        
        # runtime.txt for Heroku
        runtime_file = self.base_dir / "runtime.txt"
        with open(runtime_file, 'w') as f:
            f.write("python-3.11.0\n")
        print("✅ runtime.txt created (Heroku)")
        
        # render.yaml for Render
        render_file = self.base_dir / "render.yaml"
        render_content = """
services:
  - type: web
    name: calorietracker
    env: python
    buildCommand: pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
    startCommand: gunicorn nutrition.wsgi:application
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: nutrition.production_settings
"""
        with open(render_file, 'w') as f:
            f.write(render_content)
        print("✅ render.yaml created (Render)")
    
    def run_tests(self):
        """Run Django tests"""
        print("\n🧪 Running tests...")
        
        result = subprocess.run(
            ["python", "manage.py", "test"],
            cwd=self.base_dir
        )
        
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            return False
    
    def development_setup(self):
        """Complete development setup"""
        print("🚀 CalorieTracker Development Setup")
        print("=" * 50)
        
        steps = [
            ("Checking requirements", self.check_requirements),
            ("Setting up database", self.setup_database),
            ("Loading food data", self.load_food_data),
            ("Setting up test data", self.setup_test_data),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ Setup failed at: {step_name}")
                return False
                
        print("\n🎉 Development setup complete!")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000/")
        print("3. Login with: testuser / testpass123")
        print("4. Or create admin: python manage.py createsuperuser")
        
        return True
    
    def production_setup(self):
        """Complete production setup"""
        print("🚀 CalorieTracker Production Setup")
        print("=" * 50)
        
        steps = [
            ("Checking requirements", self.check_requirements),
            ("Setting up database", self.setup_database),
            ("Loading food data", self.load_food_data),
            ("Collecting static files", self.collect_static),
            ("Creating production settings", self.create_production_settings),
            ("Creating deployment files", self.create_deployment_files),
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                print(f"\n❌ Setup failed at: {step_name}")
                return False
                
        print("\n🎉 Production setup complete!")
        print("\nNext steps:")
        print("1. Update production_settings.py with your domain")
        print("2. Configure your production database")
        print("3. Set up your web server (nginx/apache)")
        print("4. Deploy to your hosting platform")
        
        return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python deploy.py [development|production|test]")
        sys.exit(1)
    
    config = DeploymentConfig()
    mode = sys.argv[1].lower()
    
    if mode == "development":
        success = config.development_setup()
    elif mode == "production":
        success = config.production_setup()
    elif mode == "test":
        success = config.run_tests()
    else:
        print("Invalid mode. Use: development, production, or test")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()