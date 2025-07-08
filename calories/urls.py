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