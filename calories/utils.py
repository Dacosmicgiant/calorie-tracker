from datetime import date, timedelta
from django.db.models import Sum
from .models import CalorieEntry

def get_daily_calories(user, target_date=None):
    """
    Get total calories consumed by a user on a specific date
    """
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
    """
    Get total calories for a week starting from week_start
    """
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

def get_monthly_calories(user, year=None, month=None):
    """
    Get total calories for a specific month
    """
    if year is None or month is None:
        today = date.today()
        year = today.year
        month = today.month
    
    total = CalorieEntry.objects.filter(
        user=user,
        date__year=year,
        date__month=month
    ).aggregate(
        total_calories=Sum('food__calories_per_serving')
    )['total_calories']
    
    return total or 0

def get_calorie_streak(user):
    """
    Calculate how many consecutive days the user has met their calorie goal
    """
    profile = user.userprofile
    goal = profile.daily_calorie_goal
    
    streak = 0
    current_date = date.today()
    
    while True:
        daily_calories = get_daily_calories(user, current_date)
        
        # Check if goal was met (within reasonable range)
        if daily_calories >= (goal * 0.8) and daily_calories <= (goal * 1.2):
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
        
        # Prevent infinite loop - max 365 days
        if streak >= 365:
            break
    
    return streak

def calculate_bmi(weight_kg, height_cm):
    """
    Calculate BMI (Body Mass Index)
    """
    if height_cm <= 0 or weight_kg <= 0:
        return None
    
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

def get_calorie_recommendation(age, gender, activity_level, weight_kg, height_cm):
    """
    Calculate recommended daily calories using Harris-Benedict equation
    """
    if gender.lower() == 'male':
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)
    
    # Activity level multipliers
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
    recommended_calories = bmr * multiplier
    
    return round(recommended_calories)