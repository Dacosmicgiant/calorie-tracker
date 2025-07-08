# CalorieTracker - Full Stack Web Application

A comprehensive calorie tracking web application built with Django, HTML/CSS/JavaScript, and SQLite. This project serves as a capstone project for BSc IT students, demonstrating full-stack development skills.

![CalorieTracker Dashboard](https://via.placeholder.com/800x400/4CAF50/white?text=CalorieTracker+Dashboard)

## 🌟 Features

### Core Functionality

- **User Authentication**: Secure registration, login, and logout
- **Calorie Tracking**: Add, edit, and delete daily food entries
- **Food Database**: 500+ food items with accurate nutritional data
- **Progress Monitoring**: Real-time progress bars and goal tracking
- **Data Visualization**: Interactive charts using Chart.js
- **Weekly Reports**: Comprehensive analytics and insights

### User Experience

- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **AJAX Search**: Real-time food search functionality
- **Modern UI**: Gradient backgrounds, smooth animations
- **Dark/Light Theme Elements**: Professional color scheme
- **Intuitive Navigation**: Easy-to-use interface

### Technical Features

- **CRUD Operations**: Full Create, Read, Update, Delete functionality
- **Pagination**: Efficient handling of large datasets
- **Form Validation**: Client and server-side validation
- **Session Management**: Secure user sessions
- **Static File Handling**: Optimized CSS/JS delivery

## 🛠️ Technology Stack

### Backend

- **Framework**: Django 5.2.4
- **Database**: SQLite3 (development), PostgreSQL (production ready)
- **Authentication**: Django's built-in auth system
- **API**: RESTful endpoints for AJAX functionality

### Frontend

- **Templates**: Django Template Engine
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **Charts**: Chart.js 3.9.1
- **JavaScript**: Vanilla JS with modern ES6+ features

### Development Tools

- **Version Control**: Git
- **Package Management**: pip, requirements.txt
- **Static Files**: Django's staticfiles system
- **Testing**: Django's testing framework

## 📁 Project Structure

```
nutrition/                     # Main project directory
├── nutrition/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Main settings file
│   ├── production_settings.py # Production settings
│   ├── urls.py               # Main URL configuration
│   ├── wsgi.py               # WSGI configuration
│   └── asgi.py               # ASGI configuration
├── calories/                  # Main Django app
│   ├── migrations/           # Database migrations
│   ├── static/               # Static files
│   │   └── calories/
│   │       └── css/
│   │           └── style.css # Custom CSS
│   ├── templates/            # HTML templates
│   │   ├── calories/         # App templates
│   │   └── registration/     # Auth templates
│   ├── templatetags/         # Custom template filters
│   ├── management/           # Management commands
│   │   └── commands/
│   ├── __init__.py
│   ├── admin.py              # Admin configuration
│   ├── apps.py               # App configuration
│   ├── forms.py              # Django forms
│   ├── models.py             # Database models
│   ├── signals.py            # Django signals
│   ├── tests.py              # Test suite
│   ├── urls.py               # App URL patterns
│   ├── utils.py              # Utility functions
│   └── views.py              # View functions
├── dataset.csv               # Food nutrition data
├── requirements.txt          # Python dependencies
├── manage.py                 # Django management script
├── deploy.py                 # Deployment script
├── db.sqlite3                # SQLite database
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ installed
- Git installed
- Virtual environment (recommended)

### Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd nutrition
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run setup script**

   ```bash
   python deploy.py development
   ```

5. **Start the server**

   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Open http://127.0.0.1:8000/ in your browser
   - Login with: `testuser` / `testpass123`
   - Or create admin: `python manage.py createsuperuser`

## 📖 Detailed Setup

### Manual Setup (if deploy.py doesn't work)

1. **Database Setup**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Load Food Data**

   ```bash
   python manage.py load_food_data
   ```

3. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

4. **Create Test Data**

   ```bash
   python manage.py setup_test_data --create-user --create-entries
   ```

5. **Collect Static Files** (for production)
   ```bash
   python manage.py collectstatic
   ```

## 🧪 Testing

### Run Test Suite

```bash
python manage.py test
```

### Test Individual Components

```bash
# Test models only
python manage.py test calories.tests.ModelTests

# Test views only
python manage.py test calories.tests.ViewTests

# Test forms only
python manage.py test calories.tests.FormTests
```

### Manual Testing Checklist

- ✅ User registration and authentication
- ✅ Food search and selection
- ✅ Adding/editing/deleting entries
- ✅ Dashboard data visualization
- ✅ Weekly reports generation
- ✅ Responsive design on mobile
- ✅ Form validation
- ✅ Error handling

## 📱 Usage Guide

### Getting Started

1. **Register** a new account or login
2. **Set your daily calorie goal** in profile settings
3. **Search and add foods** you consume
4. **Track your progress** on the dashboard
5. **Review weekly reports** for insights

### Key Features

#### Dashboard

- View today's calorie intake
- See progress towards daily goal
- Quick access to add new entries
- Weekly progress chart

#### Food Tracking

- Search from 500+ food items
- Real-time calorie calculations
- Edit or delete existing entries
- View complete history

#### Reports & Analytics

- Weekly calorie breakdowns
- Daily progress charts
- Goal achievement tracking
- Performance insights

## 🌐 Deployment

### Development

Already configured for local development with SQLite and debug mode enabled.

### Production Deployment

#### Option 1: PythonAnywhere

1. Upload project files
2. Create virtual environment
3. Install requirements
4. Configure WSGI file
5. Set up static files

#### Option 2: Render.com

1. Connect GitHub repository
2. Use provided `render.yaml`
3. Set environment variables
4. Deploy automatically

#### Option 3: Heroku

1. Use provided `Procfile`
2. Set environment variables
3. Configure PostgreSQL addon
4. Deploy via Git

### Environment Variables (Production)

```bash
DJANGO_SETTINGS_MODULE=nutrition.production_settings
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com
```

## 🔧 Configuration

### Settings Files

- `settings.py` - Development settings
- `production_settings.py` - Production settings (created by deploy script)

### Key Settings

- **DEBUG**: False in production
- **ALLOWED_HOSTS**: Configure for your domain
- **DATABASES**: SQLite for dev, PostgreSQL for production
- **STATIC_FILES**: Configured for both environments

### Customization

- **Colors**: Edit CSS variables in `style.css`
- **Logo/Branding**: Update templates and static files
- **Features**: Extend models and views as needed

## 📊 Database Schema

### Models Overview

#### User (Django built-in)

- username, email, password
- first_name, last_name
- date_joined, last_login

#### UserProfile

- user (OneToOne with User)
- daily_calorie_goal (Integer)
- created_at (DateTime)

#### Food

- name (CharField)
- serving (CharField)
- calories_per_serving (Integer)

#### CalorieEntry

- user (ForeignKey to User)
- food (ForeignKey to Food)
- quantity (DecimalField)
- date (DateField)
- time_added (DateTimeField)

## 🤝 Contributing

### Development Workflow

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Update documentation
6. Submit pull request

### Code Standards

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Include tests for new features
- Update README for significant changes

## 📝 API Endpoints

### Public Endpoints

- `/` - Home page
- `/login/` - User login
- `/register/` - User registration

### Authenticated Endpoints

- `/dashboard/` - Main dashboard
- `/add/` - Add calorie entry
- `/history/` - Entry history
- `/weekly-report/` - Weekly analytics
- `/profile/` - User settings

### AJAX Endpoints

- `/api/search-food/` - Food search API

## 🐛 Troubleshooting

### Common Issues

#### "No module named 'calories'"

- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

#### "Table doesn't exist" errors

- Run `python manage.py migrate`
- Check database file permissions

#### Static files not loading

- Run `python manage.py collectstatic`
- Check STATIC_URL and STATIC_ROOT settings

#### Food data missing

- Run `python manage.py load_food_data`
- Ensure `dataset.csv` exists in project root

### Debug Mode

Enable debug mode for detailed error messages:

```python
DEBUG = True  # in settings.py
```

## 📄 License

This project is developed for educational purposes as a capstone project for BSc IT students. Feel free to use and modify for learning purposes.

## 👥 Authors

- **Student Name** - Initial development
- **Course**: BSc IT Final Year
- **Institution**: [Your Institution]
- **Year**: 2025

## 🙏 Acknowledgments

- Django documentation and community
- Bootstrap and Font Awesome teams
- Chart.js developers
- Food nutrition data sources
- Course instructors and peers

## 📧 Support

For support and questions:

- Check the troubleshooting section
- Review Django documentation
- Contact course instructors
- Create issues for bugs

---

**Happy Calorie Tracking! 🍎📊**
