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