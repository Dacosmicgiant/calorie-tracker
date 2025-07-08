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