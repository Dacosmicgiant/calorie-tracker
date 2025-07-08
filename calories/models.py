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