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
        # Order foods alphabetically
        self.fields['food'].queryset = Food.objects.all().order_by('name')
        self.fields['food'].empty_label = "Select a food item..."
        
        # Set default values
        if not self.instance.pk:  # Only for new entries
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