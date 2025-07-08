# 🍎 CalorieTracker - Full Stack Web Application

[![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)](https://getbootstrap.com/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](#license)

A comprehensive calorie tracking web application built with Django, HTML/CSS/JavaScript, and SQLite. This project serves as a capstone project for BSc IT students, demonstrating full-stack development skills including modern web technologies, responsive design, and deployment practices.

![CalorieTracker Dashboard](https://via.placeholder.com/1200x600/4CAF50/white?text=CalorieTracker+Dashboard+Demo)

## 🌟 Features

### 🔐 User Management

- **Secure Registration & Authentication**: Complete user account system with session management
- **Profile Customization**: Personal settings including daily calorie goals
- **Dashboard Personalization**: Customized welcome messages and user-specific data

### 📊 Calorie Tracking

- **Comprehensive Food Database**: 500+ food items with accurate nutritional information
- **Real-time Search**: AJAX-powered food search with instant results
- **Smart Entry System**: Easy food logging with quantity and date selection
- **CRUD Operations**: Full Create, Read, Update, Delete functionality for entries

### 📈 Analytics & Visualization

- **Interactive Dashboard**: Daily progress tracking with visual indicators
- **Progress Bars**: Real-time goal achievement visualization
- **Weekly Reports**: Comprehensive analytics with Chart.js integration
- **Historical Data**: Complete entry history with pagination

### 🎨 Modern UI/UX

- **Responsive Design**: Mobile-first approach with Bootstrap 5
- **Gradient Themes**: Professional color schemes and modern aesthetics
- **Smooth Animations**: CSS transitions and hover effects
- **Intuitive Navigation**: User-friendly interface with Font Awesome icons

## 🛠️ Technology Stack

### Backend Technologies

- **Framework**: Django 5.2.4 (Python web framework)
- **Database**: SQLite3 (development), PostgreSQL (production)
- **Authentication**: Django's built-in authentication system
- **API**: RESTful endpoints for AJAX functionality
- **ORM**: Django's Object-Relational Mapping

### Frontend Technologies

- **Template Engine**: Django Template Language
- **CSS Framework**: Bootstrap 5.3.0
- **JavaScript**: Vanilla ES6+ with modern features
- **Charts**: Chart.js 3.9.1 for data visualization
- **Icons**: Font Awesome 6.4.0
- **Styling**: Custom CSS with CSS Variables and Flexbox/Grid

### Development & Deployment

- **Version Control**: Git with comprehensive .gitignore
- **Package Management**: pip with requirements.txt
- **Testing**: Django's built-in testing framework
- **Static Files**: Django's collectstatic system
- **Production Ready**: Configured for multiple hosting platforms

## 📁 Project Architecture

```
CalorieTracker/
├── 📁 nutrition/                    # Django project root
│   ├── 📄 __init__.py
│   ├── 📄 settings.py              # Development settings
│   ├── 📄 production_settings.py   # Production configuration
│   ├── 📄 urls.py                  # Main URL routing
│   ├── 📄 wsgi.py                  # WSGI configuration
│   └── 📄 asgi.py                  # ASGI configuration
├── 📁 calories/                     # Main Django application
│   ├── 📁 migrations/              # Database migrations
│   ├── 📁 static/calories/css/     # Custom stylesheets
│   ├── 📁 templates/               # HTML templates
│   │   ├── 📁 calories/            # App-specific templates
│   │   └── 📁 registration/        # Authentication templates
│   ├── 📁 management/commands/     # Custom Django commands
│   ├── 📄 models.py                # Database models
│   ├── 📄 views.py                 # View functions
│   ├── 📄 forms.py                 # Django forms
│   ├── 📄 urls.py                  # App URL patterns
│   ├── 📄 admin.py                 # Admin configuration
│   ├── 📄 signals.py               # Django signals
│   ├── 📄 utils.py                 # Utility functions
│   ├── 📄 tests.py                 # Comprehensive test suite
│   └── 📄 apps.py                  # App configuration
├── 📄 dataset.csv                  # Nutritional database (500+ foods)
├── 📄 requirements.txt             # Python dependencies
├── 📄 manage.py                    # Django management script
├── 📄 deploy.py                    # Deployment automation script
├── 📄 build.sh                     # Build script for production
├── 📄 render.yaml                  # Render.com deployment config
├── 📄 .python-version              # Python version specification
├── 📄 .gitignore                   # Git ignore patterns
└── 📄 README.md                    # This documentation
```

## 🚀 Quick Start Guide

### Prerequisites

- Python 3.8+ installed on your system
- Git for version control
- Virtual environment (recommended)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/CalorieTracker.git
   cd CalorieTracker
   ```

2. **Set Up Virtual Environment**

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # Windows:
   venv\Scripts\activate

   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Automated Setup (Recommended)**

   ```bash
   python deploy.py development
   ```

   OR **Manual Setup**:

   ```bash
   # Database setup
   python manage.py makemigrations
   python manage.py migrate

   # Load food data
   python manage.py load_food_data

   # Create test user and data
   python manage.py setup_test_data --create-user --create-entries

   # Create superuser (optional)
   python manage.py createsuperuser
   ```

5. **Start Development Server**

   ```bash
   python manage.py runserver
   ```

6. **Access the Application**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - **Test Login**: Username: `testuser`, Password: `testpass123`
   - **Admin Panel**: `http://127.0.0.1:8000/admin/` (if superuser created)

## 🧪 Testing

### Run Test Suite

```bash
# Run all tests
python manage.py test

# Run specific test categories
python manage.py test calories.tests.ModelTests
python manage.py test calories.tests.ViewTests
python manage.py test calories.tests.FormTests
python manage.py test calories.tests.IntegrationTests

# Run with coverage (if installed)
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Manual Testing Checklist

- ✅ User registration and login functionality
- ✅ Food search and entry creation
- ✅ Dashboard data visualization
- ✅ CRUD operations on calorie entries
- ✅ Weekly report generation
- ✅ Profile settings management
- ✅ Responsive design on different devices
- ✅ Form validation and error handling

## 📱 User Guide

### Getting Started

1. **Register**: Create a new account with username and password
2. **Set Goals**: Configure your daily calorie target in profile settings
3. **Search Foods**: Use the search feature to find foods from our database
4. **Log Entries**: Add foods with quantities and dates
5. **Track Progress**: Monitor your daily and weekly progress
6. **View Reports**: Analyze your nutrition patterns

### Key Features Walkthrough

#### Dashboard

- View today's calorie intake and remaining calories
- See progress bar towards daily goal
- Quick access to add new entries
- Weekly trend chart

#### Food Entry System

- Real-time search through 500+ food items
- Detailed nutritional information
- Flexible quantity input (decimals supported)
- Date selection for backdated entries

#### History & Analytics

- Paginated view of all entries
- Edit and delete capabilities
- Weekly reports with insights
- Visual progress tracking

## 🌐 Deployment Guide

### Development Environment

Already configured for local development with SQLite and debug mode.

### Production Deployment

#### Option 1: Render.com (Recommended)

1. **Push to GitHub**:

   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Render**:

   - Connect your GitHub repository
   - Set environment variables:
     ```
     DJANGO_SETTINGS_MODULE=nutrition.production_settings
     SECRET_KEY=your-secret-key-here
     ```
   - Render will automatically use `build.sh` and deploy

3. **Access Your App**: `https://your-app-name.onrender.com`

#### Option 2: Heroku

1. **Install Heroku CLI**
2. **Deploy**:
   ```bash
   heroku create your-app-name
   heroku config:set DJANGO_SETTINGS_MODULE=nutrition.production_settings
   heroku config:set SECRET_KEY=your-secret-key
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py load_food_data
   ```

#### Option 3: PythonAnywhere

1. Upload project files to PythonAnywhere
2. Create virtual environment and install requirements
3. Configure WSGI file
4. Set up static files
5. Run migrations and load data

### Environment Variables

For production deployment, set these environment variables:

```bash
SECRET_KEY=your-super-secret-key-here
DJANGO_SETTINGS_MODULE=nutrition.production_settings
DATABASE_URL=your-database-url
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DEBUG=False
```

## 🔧 Configuration & Customization

### Settings Configuration

- **Development**: `nutrition/settings.py`
- **Production**: `nutrition/production_settings.py`

### Database Configuration

```python
# Development (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production (PostgreSQL)
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}
```

### UI Customization

- **Colors**: Edit CSS variables in `calories/static/calories/css/style.css`
- **Logo**: Replace logo references in templates
- **Styling**: Modify Bootstrap classes and custom CSS

### Adding New Features

1. **Models**: Add to `calories/models.py`
2. **Views**: Add to `calories/views.py`
3. **URLs**: Add to `calories/urls.py`
4. **Templates**: Create in `calories/templates/calories/`
5. **Tests**: Add to `calories/tests.py`

## 📊 Database Schema

### Core Models

#### User (Django Built-in)

- `id` (Primary Key)
- `username` (Unique)
- `email`
- `password` (Hashed)
- `first_name`, `last_name`
- `date_joined`, `last_login`

#### UserProfile

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    daily_calorie_goal = models.IntegerField(default=2000)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### Food

```python
class Food(models.Model):
    name = models.CharField(max_length=100)
    serving = models.CharField(max_length=100)
    calories_per_serving = models.IntegerField()
```

#### CalorieEntry

```python
class CalorieEntry(models.Model):
    user = models.ForeignKey(User)
    food = models.ForeignKey(Food)
    quantity = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    time_added = models.DateTimeField(auto_now_add=True)
```

## 🔌 API Endpoints

### Authentication Required Endpoints

| Method   | Endpoint            | Description           |
| -------- | ------------------- | --------------------- |
| GET      | `/dashboard/`       | Main dashboard view   |
| GET/POST | `/add/`             | Add new calorie entry |
| GET      | `/history/`         | View entry history    |
| GET/POST | `/edit/<id>/`       | Edit specific entry   |
| POST     | `/delete/<id>/`     | Delete specific entry |
| GET/POST | `/profile/`         | User profile settings |
| GET      | `/weekly-report/`   | Weekly analytics      |
| GET      | `/api/search-food/` | AJAX food search      |

### Public Endpoints

| Method   | Endpoint     | Description       |
| -------- | ------------ | ----------------- |
| GET      | `/`          | Home page         |
| GET/POST | `/login/`    | User login        |
| GET/POST | `/register/` | User registration |
| POST     | `/logout/`   | User logout       |

## 🐛 Troubleshooting

### Common Issues & Solutions

#### "ModuleNotFoundError: No module named 'calories'"

```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Database Migration Errors

```bash
# Reset migrations (development only)
python manage.py migrate --fake calories zero
python manage.py makemigrations calories
python manage.py migrate
```

#### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --noinput

# Check settings
DEBUG = True  # for development
STATIC_URL = '/static/'
```

#### Food Data Missing

```bash
# Reload food data
python manage.py load_food_data
```

#### Permission Errors (Linux/macOS)

```bash
# Fix file permissions
chmod +x manage.py
chmod +x deploy.py
chmod +x build.sh
```

### Debug Mode

For development, enable detailed error messages:

```python
# In settings.py
DEBUG = True
```

### Logging

View application logs:

```bash
# Check Django logs
tail -f debug.log

# For production
tail -f /var/log/calorietracker/error.log
```

## 📚 Learning Objectives

This project demonstrates proficiency in:

### Backend Development

- Django framework architecture
- Model-View-Template (MVT) pattern
- Database design and ORM usage
- User authentication and authorization
- RESTful API development
- Form handling and validation

### Frontend Development

- Responsive web design principles
- Bootstrap framework usage
- JavaScript DOM manipulation
- AJAX for dynamic content
- CSS3 modern features
- Accessibility considerations

### Full-Stack Integration

- Template rendering with dynamic data
- Static file management
- Session handling
- CSRF protection
- Database migrations
- Environment configuration

### Software Engineering Practices

- Version control with Git
- Test-driven development
- Code organization and modularity
- Documentation writing
- Deployment automation
- Error handling and logging

## 🤝 Contributing

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Make** your changes
4. **Add** tests for new functionality
5. **Run** the test suite: `python manage.py test`
6. **Commit** your changes: `git commit -m "Add feature"`
7. **Push** to your fork: `git push origin feature-name`
8. **Submit** a pull request

### Code Standards

- Follow **PEP 8** for Python code style
- Use **meaningful variable names** and function names
- Add **docstrings** to all functions and classes
- Include **tests** for new features
- Update **documentation** for significant changes
- Use **type hints** where appropriate

### Commit Message Format

```
feat: add user profile picture upload
fix: resolve dashboard loading issue
docs: update installation instructions
test: add integration tests for food search
style: improve dashboard responsive layout
```

## 📄 License & Academic Use

This project is developed as a **capstone project for BSc IT students** and is intended for **educational purposes**.

### Academic Guidelines

- Feel free to use this project as a **learning reference**
- **Cite this project** if using substantial portions for academic work
- **Modify and extend** the functionality for your own projects
- **Share improvements** with the community

### Commercial Use

- Review institutional policies before commercial use
- Consider licensing requirements for production applications
- Ensure compliance with data protection regulations

## 🙏 Acknowledgments

### Technologies & Frameworks

- **Django Software Foundation** - For the excellent Django framework
- **Bootstrap Team** - For the responsive CSS framework
- **Chart.js Contributors** - For the charting library
- **Font Awesome** - For the comprehensive icon library

### Educational Support

- **Course Instructors** - For guidance and feedback
- **Peer Students** - For collaboration and code reviews
- **Stack Overflow Community** - For troubleshooting assistance
- **Django Documentation** - For comprehensive learning resources

### Data Sources

- **USDA Food Database** - For nutritional information
- **Open Food Facts** - For additional food data
- **Various Nutrition APIs** - For data validation

## 👥 Project Team

**Lead Developer**: [Your Name]  
**Course**: BSc IT Final Year  
**Institution**: [Your Institution]  
**Academic Year**: 2024-2025  
**Project Duration**: [Start Date] - [End Date]

### Supervisor

**Name**: [Supervisor Name]  
**Title**: [Title]  
**Email**: [Email]

## 📞 Support & Contact

### For Technical Issues

- 📧 **Email**: [your-email@institution.edu]
- 🐛 **Bug Reports**: Create an issue on GitHub
- 💡 **Feature Requests**: Open a discussion thread

### For Academic Inquiries

- 📚 **Course Related**: Contact your course instructor
- 🎓 **Project Evaluation**: Refer to course guidelines
- 📝 **Documentation**: Check course materials

### Community Support

- 💬 **Django Community**: [djangoproject.com/community](https://djangoproject.com/community)
- 📖 **Documentation**: [docs.djangoproject.com](https://docs.djangoproject.com)
- 🎥 **Tutorials**: Django official tutorials and YouTube channels

---

## 🎯 Project Milestones

- [x] **Phase 1**: Project setup and basic Django configuration
- [x] **Phase 2**: User authentication and profile management
- [x] **Phase 3**: Food database integration and search functionality
- [x] **Phase 4**: Calorie tracking and CRUD operations
- [x] **Phase 5**: Dashboard and data visualization
- [x] **Phase 6**: Weekly reports and analytics
- [x] **Phase 7**: UI/UX enhancements and responsive design
- [x] **Phase 8**: Testing and quality assurance
- [x] **Phase 9**: Deployment configuration and documentation
- [x] **Phase 10**: Final testing and project submission

---

**🍎 Happy Calorie Tracking! 📊**

_Built with ❤️ for BSc IT Final Year Project | Django • Bootstrap • Chart.js_
