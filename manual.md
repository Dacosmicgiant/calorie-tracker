# CalorieTracker - Complete Step-by-Step Build Guide

A comprehensive tutorial for building a full-stack calorie tracking web application using Django, HTML/CSS/JavaScript, and SQLite.

## 📋 Table of Contents

1. [Prerequisites & Environment Setup](#1-prerequisites--environment-setup)
2. [Project Initialization](#2-project-initialization)
3. [Database Models & Admin](#3-database-models--admin)
4. [Forms & Views Development](#4-forms--views-development)
5. [URL Configuration](#5-url-configuration)
6. [Template System & Frontend](#6-template-system--frontend)
7. [Static Files & Styling](#7-static-files--styling)
8. [JavaScript & AJAX Features](#8-javascript--ajax-features)
9. [Data Management & Commands](#9-data-management--commands)
10. [Testing & Quality Assurance](#10-testing--quality-assurance)

---

## 1. Prerequisites & Environment Setup

### 🎯 Learning Objectives

- Set up a Python development environment
- Understand Django project structure
- Configure virtual environments

### 📚 Required Knowledge

- Basic Python programming
- HTML, CSS, and JavaScript fundamentals
- Understanding of web development concepts
- Git version control basics

### 🛠️ System Requirements

#### Software Installation

```bash
# Check Python version (3.8+ required)
python --version

# Install pip if not available
python -m ensurepip --upgrade
```

#### Required Tools

- **Python 3.8+**
- **Git** for version control
- **Code Editor** (VS Code, PyCharm, Sublime Text)
- **Web Browser** (Chrome/Firefox for development)

### 🔧 Environment Setup

#### Step 1: Create Project Directory

```bash
mkdir calorietracker-project
cd calorietracker-project
```

#### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Verify activation (should show venv path)
which python
```

#### Step 3: Install Dependencies

```bash
# Install Django and Pillow
pip install Django==5.2.4
pip install Pillow==10.0.1

# Create requirements file
pip freeze > requirements.txt
```

---

## 2. Project Initialization

### 🎯 Learning Objectives

- Create Django project structure
- Understand Django apps concept
- Configure basic settings

### 📝 Step 1: Create Django Project

```bash
# Create main project
django-admin startproject nutrition .

# Verify project structure
ls -la
# Should see: manage.py, nutrition/
```

### 📝 Step 2: Create Django App

```bash
# Create calories app
python manage.py startapp calories

# Verify app structure
ls -la calories/
# Should see: models.py, views.py, admin.py, etc.
```

### 📝 Step 3: Create Deployment Script

Create `deploy.py`:

````python
#!/usr/bin/env python3
"""
CalorieTracker Deployment Configuration Script
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
                Initial Settings Configuration

Edit `nutrition/settings.py`:

```python
"""
Basic settings configuration
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-0&+j%jf08@g$o(t29-t4w@t!aov5vr19%u$_3k9z%he+)b@p5_"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "calories",  # Add our app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nutrition.urls"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Static files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "calories/static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Custom settings
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
````

### 📝 Step 4: Test Initial Setup

```bash
# Run initial migration
python manage.py migrate

# Test server
python manage.py runserver

# Visit http://127.0.0.1:8000/
# Should see Django welcome page
```

---

## 3. Database Models & Admin

### 🎯 Learning Objectives

- Design database schema
- Create Django models
- Set up admin interface
- Understand model relationships

### 📝 Step 1: Create Data Models

Edit `calories/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Food(models.Model):
    """Model to store food items and their nutritional information"""
    name = models.CharField(max_length=100)
    serving = models.CharField(max_length=100)
    calories_per_serving = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.calories_per_serving} cal"

    class Meta:
        ordering = ['name']

class UserProfile(models.Model):
    """Extended user profile for additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    daily_calorie_goal = models.IntegerField(default=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class CalorieEntry(models.Model):
    """Model to track daily calorie intake"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    date = models.DateField(default=timezone.now)
    time_added = models.DateTimeField(auto_now_add=True)

    @property
    def total_calories(self):
        return int(self.food.calories_per_serving * self.quantity)

    def __str__(self):
        return f"{self.user.username} - {self.food.name} - {self.total_calories} cal"

    class Meta:
        ordering = ['-time_added']
```

### 📝 Step 2: Create Model Signals

Create `calories/signals.py`:

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile whenever a new User is created"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile whenever the User is saved"""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
    else:
        UserProfile.objects.create(user=instance)
```

### 📝 Step 3: Configure App to Use Signals

Edit `calories/apps.py`:

```python
from django.apps import AppConfig

class CaloriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calories"

    def ready(self):
        import calories.signals
```

### 📝 Step 4: Set Up Admin Interface

Edit `calories/admin.py`:

```python
from django.contrib import admin
from .models import Food, UserProfile, CalorieEntry

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['name', 'serving', 'calories_per_serving']
    list_filter = ['calories_per_serving']
    search_fields = ['name']
    ordering = ['name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'daily_calorie_goal', 'created_at']
    list_filter = ['created_at']

@admin.register(CalorieEntry)
class CalorieEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'food', 'quantity', 'total_calories', 'date', 'time_added']
    list_filter = ['date', 'time_added']
    search_fields = ['user__username', 'food__name']
    date_hierarchy = 'date'

    def total_calories(self, obj):
        return obj.total_calories
    total_calories.short_description = 'Total Calories'
```

### 📝 Step 5: Create and Apply Migrations

```bash
# Create migrations
python manage.py makemigrations

# Check migration SQL (optional)
python manage.py sqlmigrate calories 0001

# Apply migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
# Follow prompts to set username, email, password
```

### 📝 Step 6: Test Admin Interface

```bash
# Start server
python manage.py runserver

# Visit http://127.0.0.1:8000/admin/
# Login with superuser credentials
# Verify all models are visible and functional
```

---

## 4. Forms & Views Development

### 🎯 Learning Objectives

- Create Django forms
- Implement CRUD operations
- Handle user authentication
- Manage form validation

### 📝 Step 1: Create Django Forms

Create `calories/forms.py`:

```python
from django import forms
from django.utils import timezone
from .models import CalorieEntry, UserProfile, Food

class CalorieEntryForm(forms.ModelForm):
    """Form for adding/editing calorie entries"""

    class Meta:
        model = CalorieEntry
        fields = ['food', 'quantity', 'date']
        widgets = {
            'food': forms.Select(attrs={
                'class': 'form-control food-select',
                'id': 'id_food'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '0.1',
                'value': '1.0'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'value': timezone.now().date().strftime('%Y-%m-%d')
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['food'].queryset = Food.objects.all().order_by('name')
        self.fields['food'].empty_label = "Select a food item..."

        if not self.instance.pk:
            self.fields['date'].initial = timezone.now().date()
            self.fields['quantity'].initial = 1.0

class UserProfileForm(forms.ModelForm):
    """Form for editing user profile settings"""

    class Meta:
        model = UserProfile
        fields = ['daily_calorie_goal']
        widgets = {
            'daily_calorie_goal': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1000',
                'max': '5000',
                'step': '50'
            })
        }
        labels = {
            'daily_calorie_goal': 'Daily Calorie Goal'
        }
        help_texts = {
            'daily_calorie_goal': 'Set your daily calorie target (1000-5000 calories)'
        }

class FoodSearchForm(forms.Form):
    """Form for searching food items"""
    search_query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search for food items...',
            'id': 'food-search'
        }),
        label='Search Food'
    )
```

### 📝 Step 2: Create Core Views

Edit `calories/views.py`:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import JsonResponse
from datetime import date, timedelta
import json

from .models import Food, CalorieEntry, UserProfile
from .forms import CalorieEntryForm, UserProfileForm

def home(request):
    """Home page - redirects to dashboard if logged in"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'calories/home.html')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, daily_calorie_goal=2000)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    """Custom login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'registration/login.html')

def user_logout(request):
    """Logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard(request):
    """Main dashboard showing today's calories and recent entries"""
    today = date.today()

    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'daily_calorie_goal': 2000}
    )

    # Get today's calorie entries
    today_entries = CalorieEntry.objects.filter(
        user=request.user,
        date=today
    ).select_related('food')

    # Calculate today's total calories
    today_calories = sum(entry.total_calories for entry in today_entries)

    # Calculate remaining calories
    remaining_calories = profile.daily_calorie_goal - today_calories

    # Get last 7 days for chart data
    week_data = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_calories = CalorieEntry.objects.filter(
            user=request.user,
            date=day
        ).aggregate(
            total=Sum('food__calories_per_serving')
        )['total'] or 0
        week_data.append({
            'date': day.strftime('%m/%d'),
            'calories': day_calories
        })

    context = {
        'profile': profile,
        'today_entries': today_entries,
        'today_calories': today_calories,
        'remaining_calories': remaining_calories,
        'calorie_goal': profile.daily_calorie_goal,
        'week_data': json.dumps(week_data),
        'progress_percentage': min(100, (today_calories / profile.daily_calorie_goal) * 100)
    }

    return render(request, 'calories/dashboard.html', context)

@login_required
def add_calorie_entry(request):
    """Add a new calorie entry"""
    if request.method == 'POST':
        form = CalorieEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, f'Added {entry.food.name} to your daily intake!')
            return redirect('dashboard')
    else:
        form = CalorieEntryForm()

    return render(request, 'calories/add_entry.html', {'form': form})

@login_required
def food_search_api(request):
    """API endpoint for food search (AJAX)"""
    query = request.GET.get('q', '')
    if len(query) >= 2:
        foods = Food.objects.filter(
            Q(name__icontains=query)
        )[:10]

        results = []
        for food in foods:
            results.append({
                'id': food.id,
                'name': food.name,
                'serving': food.serving,
                'calories': food.calories_per_serving
            })

        return JsonResponse({'results': results})

    return JsonResponse({'results': []})

@login_required
def calorie_history(request):
    """View calorie history with pagination"""
    entries = CalorieEntry.objects.filter(
        user=request.user
    ).select_related('food').order_by('-date', '-time_added')

    # Pagination
    paginator = Paginator(entries, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate daily totals
    daily_totals = {}
    for entry in page_obj:
        if entry.date not in daily_totals:
            daily_totals[entry.date] = 0
        daily_totals[entry.date] += entry.total_calories

    context = {
        'page_obj': page_obj,
        'daily_totals': daily_totals
    }

    return render(request, 'calories/history.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing calorie entry"""
    entry = get_object_or_404(CalorieEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = CalorieEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entry updated successfully!')
            return redirect('calorie_history')
    else:
        form = CalorieEntryForm(instance=entry)

    return render(request, 'calories/edit_entry.html', {'form': form, 'entry': entry})

@login_required
def delete_entry(request, entry_id):
    """Delete a calorie entry"""
    entry = get_object_or_404(CalorieEntry, id=entry_id, user=request.user)

    if request.method == 'POST':
        entry.delete()
        messages.success(request, 'Entry deleted successfully!')
        return redirect('calorie_history')

    return render(request, 'calories/delete_entry.html', {'entry': entry})

@login_required
def profile_settings(request):
    """User profile settings"""
    profile, created = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'daily_calorie_goal': 2000}
    )

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'calories/profile.html', {'form': form})

@login_required
def weekly_report(request):
    """Weekly calorie report"""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    # Get user's calorie goal
    profile = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'daily_calorie_goal': 2000}
    )[0]

    # Get this week's data
    weekly_entries = CalorieEntry.objects.filter(
        user=request.user,
        date__range=[week_start, week_end]
    ).select_related('food')

    # Organize data by day
    daily_data = {}
    for i in range(7):
        day = week_start + timedelta(days=i)
        daily_data[day] = {
            'date': day,
            'entries': [],
            'total_calories': 0,
            'day_name': day.strftime('%A')
        }

    # Populate daily data
    for entry in weekly_entries:
        if entry.date in daily_data:
            daily_data[entry.date]['entries'].append(entry)
            daily_data[entry.date]['total_calories'] += entry.total_calories

    # Calculate weekly stats
    total_week_calories = sum(day['total_calories'] for day in daily_data.values())
    avg_daily_calories = total_week_calories / 7
    goal_difference = avg_daily_calories - profile.daily_calorie_goal

    context = {
        'daily_data': daily_data,
        'week_start': week_start,
        'week_end': week_end,
        'total_week_calories': total_week_calories,
        'avg_daily_calories': avg_daily_calories,
        'daily_goal': profile.daily_calorie_goal,
        'goal_difference': goal_difference,
    }

    return render(request, 'calories/weekly_report.html', context)
```

### 📝 Step 3: Create Utility Functions

Create `calories/utils.py`:

```python
from datetime import date, timedelta
from django.db.models import Sum
from .models import CalorieEntry

def get_daily_calories(user, target_date=None):
    """Get total calories consumed by a user on a specific date"""
    if target_date is None:
        target_date = date.today()

    total = CalorieEntry.objects.filter(
        user=user,
        date=target_date
    ).aggregate(
        total_calories=Sum('food__calories_per_serving')
    )['total_calories']

    return total or 0

def get_weekly_calories(user, week_start=None):
    """Get total calories for a week starting from week_start"""
    if week_start is None:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())

    week_end = week_start + timedelta(days=6)

    total = CalorieEntry.objects.filter(
        user=user,
        date__range=[week_start, week_end]
    ).aggregate(
        total_calories=Sum('food__calories_per_serving')
    )['total_calories']

    return total or 0

def calculate_bmi(weight_kg, height_cm):
    """Calculate BMI (Body Mass Index)"""
    if height_cm <= 0 or weight_kg <= 0:
        return None

    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)
```

---

## 5. URL Configuration

### 🎯 Learning Objectives

- Configure URL routing
- Understand URL patterns
- Implement proper URL structure

### 📝 Step 1: Create App URLs

Create `calories/urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    # Home and authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Main app functionality
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_calorie_entry, name='add_entry'),
    path('history/', views.calorie_history, name='calorie_history'),
    path('profile/', views.profile_settings, name='profile_settings'),
    path('weekly-report/', views.weekly_report, name='weekly_report'),

    # CRUD operations for entries
    path('edit/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('delete/<int:entry_id>/', views.delete_entry, name='delete_entry'),

    # API endpoints
    path('api/search-food/', views.food_search_api, name='food_search_api'),
]
```

### 📝 Step 2: Update Main Project URLs

Edit `nutrition/urls.py`:

```python
"""
URL configuration for nutrition project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('calories.urls')),
]
```

### 📝 Step 3: Test URL Configuration

```bash
# Test server
python manage.py runserver

# Test URLs:
# http://127.0.0.1:8000/ (home)
# http://127.0.0.1:8000/admin/ (admin)
# http://127.0.0.1:8000/dashboard/ (should redirect to login)
```

---

## 6. Template System & Frontend

### 🎯 Learning Objectives

- Create Django templates
- Implement template inheritance
- Design responsive layouts
- Integrate Bootstrap framework

### 📝 Step 1: Create Template Directory Structure

```bash
mkdir -p calories/templates/calories
mkdir -p calories/templates/registration
```

### 📝 Step 2: Create Base Template

Create `calories/templates/calories/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}CalorieTracker{% endblock %}</title>

    <!-- Bootstrap CSS -->
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css"
      rel="stylesheet"
    />
    <!-- Font Awesome Icons -->
    <link
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
      rel="stylesheet"
    />
    <!-- Chart.js -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <!-- Custom CSS -->
    {% load static %}
    <link rel="stylesheet" href="{% static 'calories/css/style.css' %}" />

    {% block extra_css %}{% endblock %}
  </head>
  <body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
      <div class="container">
        <a class="navbar-brand" href="{% url 'home' %}">
          <i class="fas fa-utensils me-2"></i>CalorieTracker
        </a>

        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav me-auto">
            {% if user.is_authenticated %}
            <li class="nav-item">
              <a class="nav-link" href="{% url 'dashboard' %}">
                <i class="fas fa-tachometer-alt me-1"></i>Dashboard
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'add_entry' %}">
                <i class="fas fa-plus me-1"></i>Add Food
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'calorie_history' %}">
                <i class="fas fa-history me-1"></i>History
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'weekly_report' %}">
                <i class="fas fa-chart-line me-1"></i>Reports
              </a>
            </li>
            {% endif %}
          </ul>

          <ul class="navbar-nav">
            {% if user.is_authenticated %}
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                id="navbarDropdown"
                role="button"
                data-bs-toggle="dropdown"
              >
                <i class="fas fa-user me-1"></i>{{ user.username }}
              </a>
              <ul class="dropdown-menu">
                <li>
                  <a class="dropdown-item" href="{% url 'profile_settings' %}">
                    <i class="fas fa-cog me-2"></i>Settings
                  </a>
                </li>
                <li><hr class="dropdown-divider" /></li>
                <li>
                  <a class="dropdown-item" href="{% url 'logout' %}">
                    <i class="fas fa-sign-out-alt me-2"></i>Logout
                  </a>
                </li>
              </ul>
            </li>
            {% else %}
            <li class="nav-item">
              <a class="nav-link" href="{% url 'login' %}">
                <i class="fas fa-sign-in-alt me-1"></i>Login
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="{% url 'register' %}">
                <i class="fas fa-user-plus me-1"></i>Register
              </a>
            </li>
            {% endif %}
          </ul>
        </div>
      </div>
    </nav>

    <!-- Messages -->
    {% if messages %}
    <div class="container mt-3">
      {% for message in messages %}
      <div
        class="alert alert-{{ message.tags }} alert-dismissible fade show"
        role="alert"
      >
        <i class="fas fa-info-circle me-2"></i>{{ message }}
        <button
          type="button"
          class="btn-close"
          data-bs-dismiss="alert"
        ></button>
      </div>
      {% endfor %}
    </div>
    {% endif %}

    <!-- Main Content -->
    <main class="container mt-4">{% block content %}{% endblock %}</main>

    <!-- Footer -->
    <footer class="footer mt-5">
      <div class="container">
        <div class="row">
          <div class="col-md-6">
            <h5><i class="fas fa-utensils me-2"></i>CalorieTracker</h5>
            <p>Track your daily nutrition and achieve your health goals.</p>
          </div>
          <div class="col-md-6 text-md-end">
            <p>&copy; 2025 CalorieTracker. Built with Django.</p>
            <p><small>Capstone Project - BSc IT</small></p>
          </div>
        </div>
      </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>

    <!-- Custom JavaScript -->
    <script>
      // Add fade-in animation to cards
      document.addEventListener("DOMContentLoaded", function () {
        const cards = document.querySelectorAll(".card");
        cards.forEach((card, index) => {
          setTimeout(() => {
            card.classList.add("fade-in");
          }, index * 100);
        });
      });

      // Auto-hide alerts after 5 seconds
      setTimeout(function () {
        const alerts = document.querySelectorAll(".alert");
        alerts.forEach((alert) => {
          const bsAlert = new bootstrap.Alert(alert);
          bsAlert.close();
        });
      }, 5000);
    </script>

    {% block extra_js %}{% endblock %}
  </body>
</html>
```

### 📝 Step 3: Create Home Page Template

Create `calories/templates/calories/home.html`:

```html
{% extends 'calories/base.html' %} {% block title %}Welcome to CalorieTracker{%
endblock %} {% block content %}
<div class="row">
  <div class="col-lg-6">
    <div class="hero-section">
      <h1 class="display-4 fw-bold mb-4">
        <i class="fas fa-utensils text-success me-3"></i>
        Track Your Nutrition Journey
      </h1>
      <p class="lead mb-4">
        Take control of your health with our comprehensive calorie tracking
        application. Monitor your daily intake, set goals, and achieve a
        healthier lifestyle.
      </p>

      <div class="d-grid gap-2 d-md-flex justify-content-md-start">
        <a href="{% url 'register' %}" class="btn btn-primary btn-lg me-md-2">
          <i class="fas fa-rocket me-2"></i>Get Started
        </a>
        <a href="{% url 'login' %}" class="btn btn-outline-primary btn-lg">
          <i class="fas fa-sign-in-alt me-2"></i>Login
        </a>
      </div>
    </div>
  </div>

  <div class="col-lg-6">
    <div class="feature-cards">
      <div class="card mb-3">
        <div class="card-body">
          <div class="d-flex align-items-center">
            <div class="feature-icon me-3">
              <i class="fas fa-database fa-2x text-primary"></i>
            </div>
            <div>
              <h5 class="card-title mb-1">Comprehensive Food Database</h5>
              <p class="card-text text-muted">
                Access thousands of food items with accurate calorie
                information.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-body">
          <div class="d-flex align-items-center">
            <div class="feature-icon me-3">
              <i class="fas fa-chart-line fa-2x text-success"></i>
            </div>
            <div>
              <h5 class="card-title mb-1">Progress Tracking</h5>
              <p class="card-text text-muted">
                Visualize your daily, weekly, and monthly progress with charts.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div class="card mb-3">
        <div class="card-body">
          <div class="d-flex align-items-center">
            <div class="feature-icon me-3">
              <i class="fas fa-target fa-2x text-warning"></i>
            </div>
            <div>
              <h5 class="card-title mb-1">Goal Setting</h5>
              <p class="card-text text-muted">
                Set personalized calorie goals and track your achievement.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Call to Action -->
<div class="row mt-5">
  <div class="col-12">
    <div
      class="card text-center"
      style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white;"
    >
      <div class="card-body py-5">
        <h2 class="card-title">Ready to Start Your Journey?</h2>
        <p class="card-text lead">
          Join thousands of users who are already achieving their health goals.
        </p>
        <a href="{% url 'register' %}" class="btn btn-light btn-lg mt-3">
          <i class="fas fa-rocket me-2"></i>Start Tracking Today
        </a>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

### 📝 Step 4: Create Authentication Templates

Create `calories/templates/registration/login.html`:

```html
{% extends 'calories/base.html' %} {% block title %}Login - CalorieTracker{%
endblock %} {% block content %}
<div class="row justify-content-center">
  <div class="col-md-6 col-lg-4">
    <div class="card">
      <div class="card-header text-center">
        <h3><i class="fas fa-sign-in-alt me-2"></i>Welcome Back</h3>
      </div>
      <div class="card-body">
        <form method="post" novalidate>
          {% csrf_token %}

          <div class="mb-3">
            <label for="username" class="form-label">
              <i class="fas fa-user me-2"></i>Username
            </label>
            <input
              type="text"
              class="form-control"
              id="username"
              name="username"
              required
            />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">
              <i class="fas fa-lock me-2"></i>Password
            </label>
            <input
              type="password"
              class="form-control"
              id="password"
              name="password"
              required
            />
          </div>

          <div class="d-grid">
            <button type="submit" class="btn btn-primary">
              <i class="fas fa-sign-in-alt me-2"></i>Login
            </button>
          </div>
        </form>

        <hr />

        <div class="text-center">
          <p class="mb-0">Don't have an account?</p>
          <a href="{% url 'register' %}" class="btn btn-outline-primary mt-2">
            <i class="fas fa-user-plus me-2"></i>Create Account
          </a>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

Create `calories/templates/registration/register.html`:

```html
{% extends 'calories/base.html' %} {% block title %}Register - CalorieTracker{%
endblock %} {% block content %}
<div class="row justify-content-center">
  <div class="col-md-6 col-lg-5">
    <div class="card">
      <div class="card-header text-center">
        <h3><i class="fas fa-user-plus me-2"></i>Join CalorieTracker</h3>
        <p class="mb-0 text-muted">Start your nutrition journey today</p>
      </div>
      <div class="card-body">
        <form method="post" novalidate>
          {% csrf_token %}

          <div class="mb-3">
            <label for="{{ form.username.id_for_label }}" class="form-label">
              <i class="fas fa-user me-2"></i>Username
            </label>
            {{ form.username }} {% if form.username.errors %}
            <div class="text-danger small mt-1">
              {% for error in form.username.errors %}
              <div>{{ error }}</div>
              {% endfor %}
            </div>
            {% endif %}
          </div>

          <div class="mb-3">
            <label for="{{ form.password1.id_for_label }}" class="form-label">
              <i class="fas fa-lock me-2"></i>Password
            </label>
            {{ form.password1 }} {% if form.password1.errors %}
            <div class="text-danger small mt-1">
              {% for error in form.password1.errors %}
              <div>{{ error }}</div>
              {% endfor %}
            </div>
            {% endif %}
          </div>

          <div class="mb-3">
            <label for="{{ form.password2.id_for_label }}" class="form-label">
              <i class="fas fa-lock me-2"></i>Confirm Password
            </label>
            {{ form.password2 }} {% if form.password2.errors %}
            <div class="text-danger small mt-1">
              {% for error in form.password2.errors %}
              <div>{{ error }}</div>
              {% endfor %}
            </div>
            {% endif %}
          </div>

          <div class="d-grid">
            <button type="submit" class="btn btn-primary">
              <i class="fas fa-rocket me-2"></i>Create Account
            </button>
          </div>
        </form>

        <hr />

        <div class="text-center">
          <p class="mb-0">Already have an account?</p>
          <a href="{% url 'login' %}" class="btn btn-outline-primary mt-2">
            <i class="fas fa-sign-in-alt me-2"></i>Login
          </a>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %} {% block extra_js %}
<script>
  document.addEventListener("DOMContentLoaded", function () {
    // Add Bootstrap classes to Django form fields
    const formFields = document.querySelectorAll(
      'input[type="text"], input[type="password"]'
    );
    formFields.forEach((field) => {
      field.classList.add("form-control");
    });
  });
</script>
{% endblock %}
```

---

## 7. Static Files & Styling

### 🎯 Learning Objectives

- Configure static files
- Create custom CSS
- Implement responsive design
- Use CSS variables for theming

### 📝 Step 1: Create Static Files Directory

```bash
mkdir -p calories/static/calories/css
mkdir -p calories/static/calories/js
mkdir -p calories/static/calories/images
```

### 📝 Step 2: Create Custom CSS

Create `calories/static/calories/css/style.css`:

```css
/* Custom CSS for CalorieTracker Application */

:root {
  --primary-color: #4caf50;
  --secondary-color: #45a049;
  --accent-color: #ff6b6b;
  --background-color: #f8f9fa;
  --text-color: #333;
  --border-color: #dee2e6;
  --success-color: #28a745;
  --warning-color: #ffc107;
  --danger-color: #dc3545;
  --info-color: #17a2b8;
}

/* Global Styles */
body {
  background-color: var(--background-color);
  color: var(--text-color);
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
}

/* Navigation */
.navbar-custom {
  background: linear-gradient(
    135deg,
    var(--primary-color),
    var(--secondary-color)
  );
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
}

.navbar-brand {
  font-weight: bold;
  font-size: 1.5rem;
  color: white !important;
}

.navbar-nav .nav-link {
  font-weight: 500;
  margin: 0 0.5rem;
  border-radius: 20px;
  padding: 0.5rem 1rem !important;
  transition: all 0.3s ease;
  color: rgba(255, 255, 255, 0.9) !important;
}

.navbar-nav .nav-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
  color: white !important;
}

/* Cards */
.card {
  border: none;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  margin-bottom: 2rem;
}

.card:hover {
  transform: translateY(-5px);
}

.card-header {
  background: linear-gradient(
    135deg,
    var(--primary-color),
    var(--secondary-color)
  );
  color: white;
  border-radius: 15px 15px 0 0 !important;
  font-weight: 600;
  padding: 1rem 1.5rem;
}

/* Buttons */
.btn-primary {
  background: linear-gradient(
    135deg,
    var(--primary-color),
    var(--secondary-color)
  );
  border: none;
  border-radius: 25px;
  padding: 0.75rem 2rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
  background: linear-gradient(
    135deg,
    var(--secondary-color),
    var(--primary-color)
  );
}

/* Progress Bars */
.progress {
  height: 25px;
  border-radius: 15px;
  background-color: #e9ecef;
  overflow: hidden;
}

.progress-bar {
  background: linear-gradient(
    90deg,
    var(--primary-color),
    var(--secondary-color)
  );
  border-radius: 15px;
  font-weight: 600;
  transition: width 1s ease-in-out;
}

/* Forms */
.form-control {
  border-radius: 10px;
  border: 2px solid var(--border-color);
  padding: 0.75rem;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(76, 175, 80, 0.25);
  transform: translateY(-1px);
}

/* Food Items */
.food-item {
  background: white;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 0.5rem;
  border-left: 4px solid var(--primary-color);
  transition: all 0.3s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.food-item:hover {
  transform: translateX(5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

/* Search Results */
.search-results {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 10px 10px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 1000;
  display: none;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.search-result-item {
  padding: 12px 15px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s;
}

.search-result-item:hover {
  background-color: var(--background-color);
}

/* Chart Container */
.chart-container {
  position: relative;
  height: 300px;
  margin: 2rem 0;
}

/* Loading Animation */
.loading {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Fade In Animation */
.fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Footer */
.footer {
  background: linear-gradient(
    135deg,
    var(--primary-color),
    var(--secondary-color)
  );
  color: white;
  padding: 2rem 0;
  margin-top: 4rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .btn {
    width: 100%;
    margin-bottom: 0.5rem;
  }

  .chart-container {
    height: 250px;
  }
}

@media (max-width: 576px) {
  .container {
    padding: 0 10px;
  }

  .card-body {
    padding: 1rem;
  }
}
```

### 📝 Step 3: Update Settings for Static Files

Ensure your `nutrition/settings.py` includes:

```python
# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "calories/static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### 📝 Step 4: Test Static Files

```bash
# Collect static files
python manage.py collectstatic

# Start server and test
python manage.py runserver

# Visit http://127.0.0.1:8000/
# Verify CSS is loading properly
```

---

## 8. JavaScript & AJAX Features

### 🎯 Learning Objectives

- Implement AJAX functionality
- Create interactive features
- Integrate Chart.js
- Handle form validation

### 📝 Step 1: Create Dashboard Template with Charts

Create `calories/templates/calories/dashboard.html`:

```html
{% extends 'calories/base.html' %} {% block title %}Dashboard - CalorieTracker{%
endblock %} {% block content %}
<!-- Welcome Header -->
<div class="row mb-4">
  <div class="col-12">
    <div
      class="card"
      style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white;"
    >
      <div class="card-body">
        <div class="row align-items-center">
          <div class="col-md-8">
            <h2 class="mb-2">
              <i class="fas fa-sun me-2"></i>Good day, {{
              user.first_name|default:user.username }}!
            </h2>
            <p class="mb-0 lead">
              Let's track your nutrition for {% if today_entries %}{{
              today_entries.0.date|date:"F d, Y" }}{% else %}today{% endif %}
            </p>
          </div>
          <div class="col-md-4 text-md-end">
            <a href="{% url 'add_entry' %}" class="btn btn-light btn-lg">
              <i class="fas fa-plus me-2"></i>Add Food
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Stats Cards -->
<div class="row mb-4">
  <div class="col-md-3 mb-3">
    <div class="card text-center">
      <div class="card-body">
        <div class="display-6 fw-bold text-primary">{{ today_calories }}</div>
        <div class="text-muted">Calories Today</div>
        <div class="mt-2">
          <small class="text-muted">Goal: {{ calorie_goal }}</small>
        </div>
      </div>
    </div>
  </div>

  <div class="col-md-3 mb-3">
    <div class="card text-center">
      <div class="card-body">
        <div
          class="display-6 fw-bold {% if remaining_calories >= 0 %}text-success{% else %}text-danger{% endif %}"
        >
          {{ remaining_calories }}
        </div>
        <div class="text-muted">
          {% if remaining_calories >= 0 %}Remaining{% else %}Over Goal{% endif
          %}
        </div>
      </div>
    </div>
  </div>

  <div class="col-md-3 mb-3">
    <div class="card text-center">
      <div class="card-body">
        <div class="display-6 fw-bold text-info">
          {{ today_entries|length }}
        </div>
        <div class="text-muted">Food Items</div>
      </div>
    </div>
  </div>

  <div class="col-md-3 mb-3">
    <div class="card text-center">
      <div class="card-body">
        <div class="display-6 fw-bold text-warning">
          {{ progress_percentage|floatformat:0 }}%
        </div>
        <div class="text-muted">Progress</div>
      </div>
    </div>
  </div>
</div>

<!-- Progress Bar -->
<div class="row mb-4">
  <div class="col-12">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="fas fa-chart-bar me-2"></i>Daily Progress
        </h5>
      </div>
      <div class="card-body">
        <div class="d-flex justify-content-between mb-2">
          <span>{{ today_calories }} / {{ calorie_goal }} calories</span>
          <span>{{ progress_percentage|floatformat:1 }}%</span>
        </div>
        <div class="progress" style="height: 30px;">
          <div
            class="progress-bar 
                        {% if progress_percentage <= 50 %}bg-danger
                        {% elif progress_percentage <= 80 %}bg-warning
                        {% elif progress_percentage <= 100 %}bg-success
                        {% else %}bg-info
                        {% endif %}"
            role="progressbar"
            id="daily-progress-bar"
            data-progress="{{ progress_percentage|floatformat:1 }}"
          >
            <span class="fw-bold">
              {% if progress_percentage > 100 %} Over Goal! {% else %} {{
              progress_percentage|floatformat:1 }}% {% endif %}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- Today's Food Entries and Weekly Chart -->
<div class="row">
  <div class="col-lg-6 mb-4">
    <div class="card h-100">
      <div
        class="card-header d-flex justify-content-between align-items-center"
      >
        <h5 class="mb-0"><i class="fas fa-utensils me-2"></i>Today's Food</h5>
        <a href="{% url 'add_entry' %}" class="btn btn-sm btn-primary">
          <i class="fas fa-plus me-1"></i>Add
        </a>
      </div>
      <div class="card-body">
        {% if today_entries %} {% for entry in today_entries %}
        <div class="food-item mb-3">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h6 class="mb-1">{{ entry.food.name }}</h6>
              <small class="text-muted">
                {{ entry.quantity }} × {{ entry.food.serving }}
              </small>
            </div>
            <div class="text-end">
              <div class="fw-bold text-primary">
                {{ entry.total_calories }} cal
              </div>
              <div class="btn-group btn-group-sm">
                <a
                  href="{% url 'edit_entry' entry.id %}"
                  class="btn btn-outline-primary btn-sm"
                >
                  <i class="fas fa-edit"></i>
                </a>
                <a
                  href="{% url 'delete_entry' entry.id %}"
                  class="btn btn-outline-danger btn-sm"
                >
                  <i class="fas fa-trash"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
        {% endfor %} {% else %}
        <div class="text-center py-5">
          <i class="fas fa-utensils fa-3x text-muted mb-3"></i>
          <h5 class="text-muted">No food logged today</h5>
          <p class="text-muted">
            Start tracking your nutrition by adding your first meal!
          </p>
          <a href="{% url 'add_entry' %}" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>Add First Food
          </a>
        </div>
        {% endif %}
      </div>
    </div>
  </div>

  <div class="col-lg-6 mb-4">
    <div class="card h-100">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="fas fa-chart-line me-2"></i>Weekly Overview
        </h5>
      </div>
      <div class="card-body">
        <div class="chart-container">
          <canvas id="weeklyChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %} {% block extra_js %}
<script>
  document.addEventListener('DOMContentLoaded', function() {
      // Set progress bar width
      const progressBar = document.getElementById('daily-progress-bar');
      if (progressBar) {
          const progress = parseFloat(progressBar.dataset.progress) || 0;
          const width = progress > 100 ? 100 : progress;
          progressBar.style.width = width + '%';
      }

      // Weekly Chart
      const chartCanvas = document.getElementById('weeklyChart');
      if (chartCanvas && typeof Chart !== 'undefined') {
          try {
              const ctx = chartCanvas.getContext('2d');

              let weekData = [];
              let goalLine = 2000;

              {% if week_data %}
                  weekData = {{ week_data|safe }};
              {% endif %}

              {% if calorie_goal %}
                  goalLine = {{ calorie_goal }};
              {% endif %}

              if (weekData.length > 0) {
                  const chart = new Chart(ctx, {
                      type: 'line',
                      data: {
                          labels: weekData.map(function(d) { return d.date || ''; }),
                          datasets: [{
                              label: 'Daily Calories',
                              data: weekData.map(function(d) { return d.calories || 0; }),
                              borderColor: 'rgb(76, 175, 80)',
                              backgroundColor: 'rgba(76, 175, 80, 0.1)',
                              tension: 0.4,
                              fill: true
                          }, {
                              label: 'Goal',
                              data: weekData.map(function() { return goalLine; }),
                              borderColor: 'rgb(255, 193, 7)',
                              borderDash: [5, 5],
                              fill: false
                          }]
                      },
                      options: {
                          responsive: true,
                          maintainAspectRatio: false,
                          scales: {
                              y: {
                                  beginAtZero: true,
                                  title: {
                                      display: true,
                                      text: 'Calories'
                                  }
                              }
                          },
                          plugins: {
                              legend: {
                                  display: true,
                                  position: 'top'
                              }
                          }
                      }
                  });
              }
          } catch (error) {
              console.error('Error creating chart:', error);
          }
      }
  });
</script>
{% endblock %}
```

### 📝 Step 2: Create Add Entry Template with AJAX

Create `calories/templates/calories/add_entry.html`:

```html
{% extends 'calories/base.html' %} {% block title %}Add Food Entry -
CalorieTracker{% endblock %} {% block content %}
<div class="row justify-content-center">
  <div class="col-md-8">
    <div class="card">
      <div class="card-header">
        <h3><i class="fas fa-plus me-2"></i>Add Food Entry</h3>
        <p class="mb-0 text-muted">Track what you eat today</p>
      </div>
      <div class="card-body">
        <!-- Food Search -->
        <div class="mb-4">
          <label for="food-search" class="form-label">
            <i class="fas fa-search me-2"></i>Search for Food
          </label>
          <div class="position-relative">
            <input
              type="text"
              class="form-control"
              id="food-search"
              placeholder="Type to search for food items..."
              autocomplete="off"
            />
            <div id="search-results" class="search-results"></div>
          </div>
        </div>

        <!-- Form -->
        <form method="post" id="calorie-form">
          {% csrf_token %}

          <div class="row">
            <div class="col-md-6 mb-3">
              <label for="{{ form.food.id_for_label }}" class="form-label">
                <i class="fas fa-utensils me-2"></i>Selected Food
              </label>
              {{ form.food }}
              <div id="food-info" class="mt-2"></div>
            </div>

            <div class="col-md-3 mb-3">
              <label for="{{ form.quantity.id_for_label }}" class="form-label">
                <i class="fas fa-balance-scale me-2"></i>Quantity
              </label>
              {{ form.quantity }}
            </div>

            <div class="col-md-3 mb-3">
              <label for="{{ form.date.id_for_label }}" class="form-label">
                <i class="fas fa-calendar me-2"></i>Date
              </label>
              {{ form.date }}
            </div>
          </div>

          <!-- Calorie Preview -->
          <div class="row">
            <div class="col-12">
              <div
                class="card bg-light mb-3"
                id="calorie-preview"
                style="display: none;"
              >
                <div class="card-body text-center">
                  <h4 class="text-primary mb-0">
                    <i class="fas fa-fire me-2"></i>
                    <span id="total-calories">0</span> calories
                  </h4>
                  <small class="text-muted">Total for this entry</small>
                </div>
              </div>
            </div>
          </div>

          <div class="d-flex justify-content-between">
            <a href="{% url 'dashboard' %}" class="btn btn-outline-secondary">
              <i class="fas fa-arrow-left me-2"></i>Back to Dashboard
            </a>
            <button
              type="submit"
              class="btn btn-primary"
              id="submit-btn"
              disabled
            >
              <i class="fas fa-plus me-2"></i>Add Entry
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %} {% block extra_js %}
<script>
  document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("food-search");
    const searchResults = document.getElementById("search-results");
    const foodSelect = document.getElementById("id_food");
    const quantityInput = document.getElementById("id_quantity");
    const foodInfo = document.getElementById("food-info");
    const caloriePreview = document.getElementById("calorie-preview");
    const totalCaloriesSpan = document.getElementById("total-calories");
    const submitBtn = document.getElementById("submit-btn");

    let searchTimeout;
    let selectedFood = null;

    // Food search functionality
    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimeout);
      const query = this.value.trim();

      if (query.length < 2) {
        searchResults.style.display = "none";
        return;
      }

      searchTimeout = setTimeout(() => {
        fetch(`/api/search-food/?q=${encodeURIComponent(query)}`)
          .then((response) => response.json())
          .then((data) => {
            displaySearchResults(data.results);
          })
          .catch((error) => {
            console.error("Search error:", error);
          });
      }, 300);
    });

    function displaySearchResults(results) {
      searchResults.innerHTML = "";

      if (results.length === 0) {
        searchResults.innerHTML =
          '<div class="search-result-item">No foods found</div>';
      } else {
        results.forEach((food) => {
          const item = document.createElement("div");
          item.className = "search-result-item";
          item.innerHTML = `
                    <div class="search-result-name">${food.name}</div>
                    <div class="search-result-details">
                        ${food.serving} - <span class="search-result-calories">${food.calories} cal</span>
                    </div>
                `;

          item.addEventListener("click", () => {
            selectFood(food);
          });

          searchResults.appendChild(item);
        });
      }

      searchResults.style.display = "block";
    }

    function selectFood(food) {
      selectedFood = food;
      searchInput.value = food.name;
      searchResults.style.display = "none";

      // Update the select dropdown
      foodSelect.value = food.id;

      // Show food info
      foodInfo.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>${food.name}</strong><br>
                    <small class="text-muted">${food.serving}</small>
                </div>
                <div class="text-end">
                    <div class="h5 text-primary mb-0">${food.calories} cal</div>
                    <small class="text-muted">per serving</small>
                </div>
            </div>
        `;

      updateCaloriePreview();
      checkFormValid();
    }

    function updateCaloriePreview() {
      if (selectedFood && quantityInput.value) {
        const quantity = parseFloat(quantityInput.value) || 1;
        const totalCalories = Math.round(selectedFood.calories * quantity);

        totalCaloriesSpan.textContent = totalCalories;
        caloriePreview.style.display = "block";
      } else {
        caloriePreview.style.display = "none";
      }
    }

    function checkFormValid() {
      const isValid =
        selectedFood &&
        quantityInput.value &&
        document.getElementById("id_date").value;
      submitBtn.disabled = !isValid;
    }

    // Update calorie preview when quantity changes
    quantityInput.addEventListener("input", function () {
      updateCaloriePreview();
      checkFormValid();
    });

    // Update validation when date changes
    document
      .getElementById("id_date")
      .addEventListener("change", checkFormValid);

    // Hide search results when clicking outside
    document.addEventListener("click", function (e) {
      if (
        !searchInput.contains(e.target) &&
        !searchResults.contains(e.target)
      ) {
        searchResults.style.display = "none";
      }
    });

    // Form submission
    document
      .getElementById("calorie-form")
      .addEventListener("submit", function (e) {
        if (!selectedFood) {
          e.preventDefault();
          alert("Please select a food item");
          return;
        }

        // Show loading state
        submitBtn.innerHTML = '<span class="loading"></span> Adding...';
        submitBtn.disabled = true;
      });
  });
</script>
{% endblock %}
```

---

## 9. Data Management & Commands

### 🎯 Learning Objectives

- Create Django management commands
- Load data from CSV files
- Implement data validation
- Set up test data

### 📝 Step 1: Create Management Commands Directory

```bash
mkdir -p calories/management
mkdir -p calories/management/commands
touch calories/management/__init__.py
touch calories/management/commands/__init__.py
```

### 📝 Step 2: Create Food Data Loading Command

Create `calories/management/commands/load_food_data.py`:

```python
import csv
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from calories.models import Food

class Command(BaseCommand):
    help = 'Load food data from CSV file'

    def handle(self, *args, **options):
        # Path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'dataset.csv')

        if not os.path.exists(csv_file_path):
            self.stdout.write(
                self.style.ERROR('CSV file not found at: %s' % csv_file_path)
            )
            return

        # Clear existing food data
        Food.objects.all().delete()
        self.stdout.write('Cleared existing food data')

        # Load data from CSV
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            foods_created = 0

            for row in reader:
                try:
                    # Extract calories from the string
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
                    self.stdout.write(
                        self.style.WARNING(
                            'Skipped row for %s: %s' % (row.get('Food', 'Unknown'), str(e))
                        )
                    )
                    continue

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully loaded %d food items' % foods_created
            )
        )
```

### 📝 Step 3: Create Test Data Setup Command

Create `calories/management/commands/setup_test_data.py`:

```python
import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from calories.models import Food, UserProfile, CalorieEntry

class Command(BaseCommand):
    help = 'Set up test data for CalorieTracker application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-user',
            action='store_true',
            help='Create a test user',
        )
        parser.add_argument(
            '--create-entries',
            action='store_true',
            help='Create sample calorie entries',
        )
        parser.add_argument(
            '--username',
            type=str,
            default='testuser',
            help='Username for test user',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='testpass123',
            help='Password for test user',
        )

    def handle(self, *args, **options):
        self.stdout.write('Setting up test data...')

        # Verify food data exists
        food_count = Food.objects.count()
        if food_count == 0:
            self.stdout.write(
                self.style.WARNING(
                    'No food data found. Run: python manage.py load_food_data'
                )
            )
            return

        # Create test user if requested
        if options['create_user']:
            username = options['username']
            password = options['password']

            if User.objects.filter(username=username).exists():
                self.stdout.write(f'User "{username}" already exists')
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=f'{username}@example.com',
                    first_name='Test',
                    last_name='User'
                )
                self.stdout.write(f'Created test user: {username}')

            # Create user profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'daily_calorie_goal': 2200}
            )

            # Create sample entries if requested
            if options['create_entries']:
                self.create_sample_entries(user)

        self.display_summary()

    def create_sample_entries(self, user):
        """Create sample calorie entries for the past week"""
        self.stdout.write('Creating sample calorie entries...')

        foods = list(Food.objects.all()[:50])
        entries_created = 0

        # Create entries for the past 7 days
        for days_back in range(7):
            entry_date = date.today() - timedelta(days=days_back)
            daily_entries = random.randint(2, 5)

            for _ in range(daily_entries):
                food = random.choice(foods)
                quantity = round(random.uniform(0.5, 2.5), 1)

                if not CalorieEntry.objects.filter(
                    user=user,
                    food=food,
                    date=entry_date
                ).exists():
                    CalorieEntry.objects.create(
                        user=user,
                        food=food,
                        quantity=quantity,
                        date=entry_date
                    )
                    entries_created += 1

        self.stdout.write(f'Created {entries_created} sample entries')

    def display_summary(self):
        """Display a summary of the current data"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('DATABASE SUMMARY')
        self.stdout.write('='*50)

        food_count = Food.objects.count()
        user_count = User.objects.count()
        entry_count = CalorieEntry.objects.count()

        self.stdout.write(f'Food items: {food_count}')
        self.stdout.write(f'Users: {user_count}')
        self.stdout.write(f'Calorie entries: {entry_count}')

        self.stdout.write('\nNEXT STEPS:')
        self.stdout.write('1. Run: python manage.py runserver')
        self.stdout.write('2. Visit: http://127.0.0.1:8000/')
        self.stdout.write('3. Login with: testuser / testpass123')
        self.stdout.write('='*50)
```

### 📝 Step 4: Create Dataset CSV File

Create `dataset.csv` in your project root:

```csv
Food,Serving,Calories
Apple,1 medium (182 g),95 cal
Banana,1 medium (125 g),111 cal
Orange,1 medium (131 g),62 cal
Grapes,1 cup (151 g),104 cal
Strawberries,1 cup (152 g),49 cal
Blueberries,1 cup (148 g),84 cal
Chicken Breast,1 piece (71 g),116 cal
Salmon,1 fillet (198 g),367 cal
Tuna,1 can (154 g),191 cal
Beef,1 oz (28 g),75 cal
Pork,1 oz (28 g),78 cal
Rice,1 cup (195 g),757 cal
Bread,1 slice (28 g),79 cal
Pasta,2 oz (56 g),207 cal
Potato,1 medium (213 g),164 cal
Broccoli,1 cup (91 g),25 cal
Carrots,1 medium (61 g),25 cal
Spinach,1 cup (30 g),7 cal
Milk,1 cup (244 g),149 cal
Cheese,1 oz (28 g),113 cal
Yogurt,1 cup (245 g),154 cal
Eggs,1 large (50 g),70 cal
Almonds,1 oz (28 g),164 cal
Peanuts,1 oz (28 g),161 cal
Avocado,1 medium (200 g),320 cal
```

### 📝 Step 5: Load Data and Test

```bash
# Load food data
python manage.py load_food_data

# Create test user and entries
python manage.py setup_test_data --create-user --create-entries

# Verify data loaded
python manage.py shell
>>> from calories.models import Food, CalorieEntry
>>> Food.objects.count()
>>> CalorieEntry.objects.count()
>>> exit()
```

---

## 10. Testing & Quality Assurance

### 🎯 Learning Objectives

- Write comprehensive tests
- Test models, views, and forms
- Implement integration testing
- Use Django testing framework

### 📝 Step 1: Create Comprehensive Test Suite

Edit `calories/tests.py`:

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
import json

from .models import Food, UserProfile, CalorieEntry
from .forms import CalorieEntryForm, UserProfileForm

class ModelTests(TestCase):
    """Test all models and their methods"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )

        self.food = Food.objects.create(
            name='Test Apple',
            serving='1 medium (180g)',
            calories_per_serving=95
        )

    def test_food_model(self):
        """Test Food model"""
        self.assertEqual(str(self.food), 'Test Apple - 95 cal')
        self.assertEqual(self.food.name, 'Test Apple')
        self.assertEqual(self.food.calories_per_serving, 95)

    def test_user_profile_creation(self):
        """Test UserProfile model"""
        profile = UserProfile.objects.create(
            user=self.user,
            daily_calorie_goal=2200
        )

        self.assertEqual(str(profile), "testuser's Profile")
        self.assertEqual(profile.daily_calorie_goal, 2200)

    def test_calorie_entry_model(self):
        """Test CalorieEntry model"""
        entry = CalorieEntry.objects.create(
            user=self.user,
            food=self.food,
            quantity=1.5,
            date=date.today()
        )

        self.assertEqual(entry.total_calories, 142)  # 95 * 1.5
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.food, self.food)

class ViewTests(TestCase):
    """Test all views and their functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.profile = UserProfile.objects.create(
            user=self.user,
            daily_calorie_goal=2000
        )

        self.food = Food.objects.create(
            name='Test Food',
            serving='1 serving',
            calories_per_serving=100
        )

    def test_home_view(self):
        """Test home page"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'CalorieTracker')

    def test_login_view(self):
        """Test login functionality"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')

    def test_dashboard_view(self):
        """Test dashboard for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_add_entry_view(self):
        """Test adding calorie entry"""
        self.client.login(username='testuser', password='testpass123')

        response = self.client.post(reverse('add_entry'), {
            'food': self.food.id,
            'quantity': 1.0,
            'date': date.today()
        })

        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(CalorieEntry.objects.filter(user=self.user).exists())

    def test_food_search_api(self):
        """Test food search API"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('food_search_api'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)
        self.assertIn('results', data)

class FormTests(TestCase):
    """Test all forms"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.food = Food.objects.create(
            name='Test Food',
            serving='1 serving',
            calories_per_serving=100
        )

    def test_calorie_entry_form_valid(self):
        """Test valid CalorieEntryForm"""
        form_data = {
            'food': self.food.id,
            'quantity': 1.5,
            'date': date.today()
        }

        form = CalorieEntryForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_calorie_entry_form_invalid(self):
        """Test invalid CalorieEntryForm"""
        form_data = {
            'food': '',
            'quantity': -1,
            'date': date.today()
        }

        form = CalorieEntryForm(data=form_data)
        self.assertFalse(form.is_valid())

class IntegrationTests(TestCase):
    """Test complete user workflows"""

    def setUp(self):
        self.client = Client()

        # Create test foods
        foods_data = [
            ('Apple', '1 medium', 95),
            ('Banana', '1 medium', 105),
            ('Orange', '1 medium', 62),
        ]

        for name, serving, calories in foods_data:
            Food.objects.create(
                name=name,
                serving=serving,
                calories_per_serving=calories
            )

    def test_complete_user_journey(self):
        """Test complete user journey from registration to tracking"""

        # Register user
        response = self.client.post(reverse('register'), {
            'username': 'journeyuser',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        })
        self.assertRedirects(response, reverse('login'))

        # Login
        response = self.client.post(reverse('login'), {
            'username': 'journeyuser',
            'password': 'complexpass123'
        })
        self.assertRedirects(response, reverse('dashboard'))

        # Add entry
        apple = Food.objects.get(name='Apple')
        response = self.client.post(reverse('add_entry'), {
            'food': apple.id,
            'quantity': 1.0,
            'date': date.today()
        })
        self.assertRedirects(response, reverse('dashboard'))

        # Verify entry exists
        user = User.objects.get(username='journeyuser')
        self.assertTrue(CalorieEntry.objects.filter(user=user, food=apple).exists())
```

### 📝 Step 2: Run Tests

```bash
# Run all tests
python manage.py test

# Run specific test class
python manage.py test calories.tests.ModelTests

# Run with verbose output
python manage.py test --verbosity=2

# Generate coverage report (install coverage first)
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Creates htmlcov/ directory
```

### 📝 Step 3: Manual Testing Checklist

Create a manual testing checklist:

```markdown
## Manual Testing Checklist

### Authentication

- [ ] User can register with valid credentials
- [ ] User cannot register with invalid/duplicate credentials
- [ ] User can login with correct credentials
- [ ] User cannot login with incorrect credentials
- [ ] User can logout successfully
- [ ] Logged out user is redirected to login for protected pages

### Dashboard

- [ ] Dashboard shows correct user information
- [ ] Today's calorie count is accurate
- [ ] Progress bar displays correctly
- [ ] Charts render properly
- [ ] Quick action buttons work

### Food Tracking

- [ ] Food search returns relevant results
- [ ] User can select food from search results
- [ ] Calorie preview updates correctly
- [ ] Entry is saved successfully
- [ ] User can edit existing entries
- [ ] User can delete entries with confirmation

### Navigation

- [ ] All navigation links work
- [ ] Responsive design works on mobile
- [ ] Dropdown menus function properly

### Data Validation

- [ ] Forms validate required fields
- [ ] Forms reject invalid data
- [ ] Error messages display clearly
- [ ] Success messages appear after actions

### Performance

- [ ] Pages load quickly
- [ ] AJAX requests respond promptly
- [ ] No JavaScript errors in console
- [ ] Images and static files load properly
```

---
