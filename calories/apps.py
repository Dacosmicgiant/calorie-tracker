# calories/apps.py
from django.apps import AppConfig


class CaloriesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "calories"
    
    def ready(self):
        """Import signals when the app is ready"""
        try:
            import calories.signals
        except ImportError:
            pass