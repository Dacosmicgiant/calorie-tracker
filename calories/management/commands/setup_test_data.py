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
            help='Username for test user (default: testuser)',
        )
        parser.add_argument(
            '--password',
            type=str,
            default='testpass123',
            help='Password for test user (default: testpass123)',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Setting up CalorieTracker test data...')
        )

        # Verify food data exists
        food_count = Food.objects.count()
        if food_count == 0:
            self.stdout.write(
                self.style.WARNING(
                    'No food data found. Please run: python manage.py load_food_data'
                )
            )
            return

        self.stdout.write(f'Found {food_count} food items in database')

        # Create test user if requested
        if options['create_user']:
            username = options['username']
            password = options['password']
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User "{username}" already exists')
                )
                user = User.objects.get(username=username)
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=f'{username}@example.com',
                    first_name='Test',
                    last_name='User'
                )
                self.stdout.write(
                    self.style.SUCCESS(f'Created test user: {username}')
                )

            # Create or update user profile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'daily_calorie_goal': 2200}
            )
            
            if created:
                self.stdout.write('Created user profile')
            else:
                self.stdout.write('User profile already exists')

            # Create sample entries if requested
            if options['create_entries']:
                self.create_sample_entries(user)

        # Display summary
        self.display_summary()

    def create_sample_entries(self, user):
        """Create sample calorie entries for the past week"""
        self.stdout.write('Creating sample calorie entries...')
        
        # Get random food items
        foods = list(Food.objects.all()[:50])  # Use first 50 foods
        entries_created = 0
        
        # Create entries for the past 7 days
        for days_back in range(7):
            entry_date = date.today() - timedelta(days=days_back)
            
            # Create 2-5 random entries per day
            daily_entries = random.randint(2, 5)
            
            for _ in range(daily_entries):
                # Select random food and quantity
                food = random.choice(foods)
                quantity = round(random.uniform(0.5, 2.5), 1)
                
                # Check if entry already exists to avoid duplicates
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

        self.stdout.write(
            self.style.SUCCESS(f'Created {entries_created} sample entries')
        )

    def display_summary(self):
        """Display a summary of the current data"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('DATABASE SUMMARY'))
        self.stdout.write('='*50)
        
        # Food data
        food_count = Food.objects.count()
        self.stdout.write(f'Food items: {food_count}')
        
        # User data
        user_count = User.objects.count()
        self.stdout.write(f'Users: {user_count}')
        
        # Profile data
        profile_count = UserProfile.objects.count()
        self.stdout.write(f'User profiles: {profile_count}')
        
        # Entry data
        entry_count = CalorieEntry.objects.count()
        self.stdout.write(f'Calorie entries: {entry_count}')
        
        # Recent entries
        recent_entries = CalorieEntry.objects.select_related('user', 'food').order_by('-time_added')[:5]
        
        if recent_entries:
            self.stdout.write('\nRecent entries:')
            for entry in recent_entries:
                self.stdout.write(
                    f'  {entry.user.username}: {entry.food.name} '
                    f'({entry.total_calories} cal) - {entry.date}'
                )
        
        self.stdout.write('\n' + '='*50)
        
        # Test user login info
        test_users = User.objects.filter(username__in=['testuser', 'admin'])
        if test_users.exists():
            self.stdout.write(self.style.SUCCESS('TEST LOGIN CREDENTIALS:'))
            for user in test_users:
                if user.username == 'testuser':
                    self.stdout.write(f'Username: {user.username}')
                    self.stdout.write('Password: testpass123')
                elif user.is_superuser:
                    self.stdout.write(f'Admin: {user.username}')
                    self.stdout.write('(Use your admin password)')
            self.stdout.write('='*50)
        
        # Next steps
        self.stdout.write(self.style.SUCCESS('NEXT STEPS:'))
        self.stdout.write('1. Run: python manage.py runserver')
        self.stdout.write('2. Visit: http://127.0.0.1:8000/')
        self.stdout.write('3. Login with test credentials above')
        self.stdout.write('4. Start tracking calories!')
        self.stdout.write('='*50)