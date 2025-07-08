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
import logging

from .models import Food, CalorieEntry, UserProfile
from .forms import CalorieEntryForm, UserProfileForm

# Get logger for this module
logger = logging.getLogger(__name__)

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
            try:
                user = form.save()
                # UserProfile will be created automatically by signal handler
                # No need to create it manually here
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                return redirect('login')
            except Exception as e:
                # Log the error and show a user-friendly message
                logger.error(f'Error creating user account: {e}')
                messages.error(request, 'An error occurred while creating your account. Please try again.')
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
            try:
                entry = form.save(commit=False)
                entry.user = request.user
                entry.save()
                messages.success(request, f'Added {entry.food.name} to your daily intake!')
                return redirect('dashboard')
            except Exception as e:
                logger.error(f'Error adding calorie entry for user {request.user.username}: {e}')
                messages.error(request, 'An error occurred while adding your entry. Please try again.')
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
    paginator = Paginator(entries, 15)  # Show 15 entries per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate daily totals for displayed entries
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
            try:
                form.save()
                messages.success(request, 'Entry updated successfully!')
                return redirect('calorie_history')
            except Exception as e:
                logger.error(f'Error updating entry {entry_id} for user {request.user.username}: {e}')
                messages.error(request, 'An error occurred while updating your entry. Please try again.')
    else:
        form = CalorieEntryForm(instance=entry)
    
    return render(request, 'calories/edit_entry.html', {'form': form, 'entry': entry})

@login_required
def delete_entry(request, entry_id):
    """Delete a calorie entry"""
    entry = get_object_or_404(CalorieEntry, id=entry_id, user=request.user)
    
    if request.method == 'POST':
        try:
            food_name = entry.food.name
            entry.delete()
            messages.success(request, f'Entry for {food_name} deleted successfully!')
            return redirect('calorie_history')
        except Exception as e:
            logger.error(f'Error deleting entry {entry_id} for user {request.user.username}: {e}')
            messages.error(request, 'An error occurred while deleting your entry. Please try again.')
    
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
            try:
                form.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('dashboard')
            except Exception as e:
                logger.error(f'Error updating profile for user {request.user.username}: {e}')
                messages.error(request, 'An error occurred while updating your profile. Please try again.')
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