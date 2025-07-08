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
        self.assertEqual(profile.user, self.user)
    
    def test_calorie_entry_model(self):
        """Test CalorieEntry model"""
        entry = CalorieEntry.objects.create(
            user=self.user,
            food=self.food,
            quantity=1.5,
            date=date.today()
        )
        
        self.assertEqual(entry.total_calories, 142)  # 95 * 1.5 = 142.5, rounded to 142
        self.assertEqual(str(entry), 'testuser - Test Apple - 142 cal')
        self.assertEqual(entry.user, self.user)
        self.assertEqual(entry.food, self.food)

class ViewTests(TestCase):
    """Test all views and their functionality"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
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
    
    def test_home_redirect_when_authenticated(self):
        """Test home redirects to dashboard when user is logged in"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_login_view(self):
        """Test login functionality"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')
    
    def test_register_view(self):
        """Test user registration"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')
    
    def test_dashboard_view(self):
        """Test dashboard for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Good day')
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
        self.assertTrue(CalorieEntry.objects.filter(user=self.user, food=self.food).exists())
    
    def test_calorie_history_view(self):
        """Test calorie history page"""
        self.client.login(username='testuser', password='testpass123')
        
        # Create a test entry
        CalorieEntry.objects.create(
            user=self.user,
            food=self.food,
            quantity=1.0,
            date=date.today()
        )
        
        response = self.client.get(reverse('calorie_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Food')
    
    def test_weekly_report_view(self):
        """Test weekly report page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('weekly_report'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Weekly Report')
    
    def test_profile_settings_view(self):
        """Test profile settings page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile_settings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile Settings')
    
    def test_food_search_api(self):
        """Test food search API"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('food_search_api'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['name'], 'Test Food')

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
            'quantity': -1,  # Invalid quantity
            'date': date.today()
        }
        
        form = CalorieEntryForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_user_profile_form_valid(self):
        """Test valid UserProfileForm"""
        profile = UserProfile.objects.create(
            user=self.user,
            daily_calorie_goal=2000
        )
        
        form_data = {
            'daily_calorie_goal': 2200
        }
        
        form = UserProfileForm(data=form_data, instance=profile)
        self.assertTrue(form.is_valid())
    
    def test_user_profile_form_invalid(self):
        """Test invalid UserProfileForm"""
        form_data = {
            'daily_calorie_goal': 500  # Too low
        }
        
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

class IntegrationTests(TestCase):
    """Test complete user workflows"""
    
    def setUp(self):
        self.client = Client()
        
        # Create test foods
        foods_data = [
            ('Apple', '1 medium (180g)', 95),
            ('Banana', '1 medium (120g)', 105),
            ('Orange', '1 medium (154g)', 62),
        ]
        
        for name, serving, calories in foods_data:
            Food.objects.create(
                name=name,
                serving=serving,
                calories_per_serving=calories
            )
    
    def test_complete_user_journey(self):
        """Test a complete user journey from registration to tracking"""
        
        # 1. Register a new user
        response = self.client.post(reverse('register'), {
            'username': 'journeyuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123'
        })
        self.assertRedirects(response, reverse('login'))
        
        # 2. Login
        response = self.client.post(reverse('login'), {
            'username': 'journeyuser',
            'password': 'complexpassword123'
        })
        self.assertRedirects(response, reverse('dashboard'))
        
        # 3. View dashboard (should be empty initially)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No food logged today')
        
        # 4. Add a food entry
        apple = Food.objects.get(name='Apple')
        response = self.client.post(reverse('add_entry'), {
            'food': apple.id,
            'quantity': 1.0,
            'date': date.today()
        })
        self.assertRedirects(response, reverse('dashboard'))
        
        # 5. View dashboard again (should show the entry)
        response = self.client.get(reverse('dashboard'))
        self.assertContains(response, 'Apple')
        self.assertContains(response, '95')  # calories
        
        # 6. Add another entry
        banana = Food.objects.get(name='Banana')
        response = self.client.post(reverse('add_entry'), {
            'food': banana.id,
            'quantity': 2.0,
            'date': date.today()
        })
        
        # 7. Check history
        response = self.client.get(reverse('calorie_history'))
        self.assertContains(response, 'Apple')
        self.assertContains(response, 'Banana')
        
        # 8. View weekly report
        response = self.client.get(reverse('weekly_report'))
        self.assertEqual(response.status_code, 200)
        
        # 9. Update profile settings
        response = self.client.post(reverse('profile_settings'), {
            'daily_calorie_goal': 2200
        })
        self.assertRedirects(response, reverse('dashboard'))
        
        # 10. Verify the goal was updated
        user = User.objects.get(username='journeyuser')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.daily_calorie_goal, 2200)
    
    def test_food_search_workflow(self):
        """Test food search functionality"""
        # Create user and login
        user = User.objects.create_user('searchuser', password='testpass123')
        self.client.login(username='searchuser', password='testpass123')
        
        # Search for foods
        response = self.client.get(reverse('food_search_api'), {'q': 'app'})
        data = json.loads(response.content)
        
        # Should find Apple
        self.assertTrue(any(result['name'] == 'Apple' for result in data['results']))
    
    def test_entry_crud_operations(self):
        """Test Create, Read, Update, Delete operations for entries"""
        # Setup
        user = User.objects.create_user('cruduser', password='testpass123')
        self.client.login(username='cruduser', password='testpass123')
        
        apple = Food.objects.get(name='Apple')
        
        # Create
        response = self.client.post(reverse('add_entry'), {
            'food': apple.id,
            'quantity': 1.0,
            'date': date.today()
        })
        self.assertRedirects(response, reverse('dashboard'))
        
        entry = CalorieEntry.objects.get(user=user, food=apple)
        
        # Read (via history)
        response = self.client.get(reverse('calorie_history'))
        self.assertContains(response, 'Apple')
        
        # Update
        response = self.client.post(reverse('edit_entry', args=[entry.id]), {
            'food': apple.id,
            'quantity': 2.0,
            'date': date.today()
        })
        self.assertRedirects(response, reverse('calorie_history'))
        
        entry.refresh_from_db()
        self.assertEqual(float(entry.quantity), 2.0)
        
        # Delete
        response = self.client.post(reverse('delete_entry', args=[entry.id]))
        self.assertRedirects(response, reverse('calorie_history'))
        
        self.assertFalse(CalorieEntry.objects.filter(id=entry.id).exists())

class PerformanceTests(TestCase):
    """Test application performance with larger datasets"""
    
    def setUp(self):
        self.user = User.objects.create_user('perfuser', password='testpass123')
        self.client = Client()
        self.client.login(username='perfuser', password='testpass123')
        
        # Create many food items
        for i in range(100):
            Food.objects.create(
                name=f'Food Item {i}',
                serving=f'1 serving ({i*10}g)',
                calories_per_serving=100 + i
            )
    
    def test_food_search_performance(self):
        """Test food search with many items"""
        response = self.client.get(reverse('food_search_api'), {'q': 'Food'})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        # Should limit results to 10
        self.assertLessEqual(len(data['results']), 10)
    
    def test_history_pagination(self):
        """Test history page with many entries"""
        foods = Food.objects.all()[:20]
        
        # Create many entries
        for i in range(50):
            food = foods[i % len(foods)]
            CalorieEntry.objects.create(
                user=self.user,
                food=food,
                quantity=1.0,
                date=date.today() - timedelta(days=i//5)
            )
        
        response = self.client.get(reverse('calorie_history'))
        self.assertEqual(response.status_code, 200)
        
        # Should have pagination
        self.assertContains(response, 'pagination')

def run_manual_tests():
    """Manual test checklist - not automated"""
    checklist = [
        "✓ Home page loads correctly",
        "✓ User can register successfully", 
        "✓ User can login/logout",
        "✓ Dashboard shows current day's calories",
        "✓ Food search works with AJAX",
        "✓ Can add food entries",
        "✓ Can edit food entries",
        "✓ Can delete food entries",
        "✓ History page shows all entries",
        "✓ Weekly report displays charts",
        "✓ Profile settings can be updated",
        "✓ Responsive design works on mobile",
        "✓ Charts render correctly",
        "✓ Form validation works",
        "✓ Error messages display properly",
        "✓ Success messages display properly",
        "✓ Navigation works correctly",
        "✓ Static files load properly",
        "✓ Admin interface accessible",
        "✓ Food data loaded correctly"
    ]
    
    print("Manual Test Checklist:")
    print("=" * 30)
    for item in checklist:
        print(item)
    print("=" * 30)
    print("Please verify each item manually by using the application.")