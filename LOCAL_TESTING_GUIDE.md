# Local Testing Guide

## ✅ Setup Complete

Your versity_farewell backend is now running locally and ready for testing!

### 📊 Current Status

- ✅ Django 4.2.8 backend server running
- ✅ Database migrations applied (SQLite)
- ✅ Admin panel configured
- ✅ All models created (Users, Timeline, Responsibilities)
- ✅ Serializers and validation ready
- ✅ 8/8 unit tests passing
- ✅ JWT authentication configured
- ✅ Docker infrastructure ready (when daemon available)
- ✅ GitHub repository synced

### 🌐 Access Points

#### Admin Dashboard
- **URL**: http://localhost:8000/admin
- **Email**: `admin@farewell.local`
- **Password**: `admin123`
- Features:
  - User management with roles
  - Timeline creation and events
  - Responsibility assignment
  - Permission management

#### Django Shell (for manual testing)
```bash
cd backend
"/home/alamin/Desktop/Others Projects/versity_farewell/.venv/bin/python" manage.py shell
```

#### API Endpoints (to be created in Phase 3)
```
POST   /api/auth/register         - User registration
POST   /api/auth/login            - User login
POST   /api/auth/logout           - User logout
POST   /api/auth/verify-email     - Email verification
GET    /api/users/profile         - Get user profile
PUT    /api/users/profile         - Update user profile
GET    /api/timeline              - List timelines
POST   /api/timeline              - Create timeline
GET    /api/responsibilities      - List responsibilities
POST   /api/responsibilities      - Create responsibility
```

### 📝 Test Data Creation

Create test data in Django shell:

```python
from users.models import CustomUser, Role
from timeline.models import Timeline, TimelineEvent
from responsibilities.models import Responsibility, ResponsibilityCategory

# Create roles
admin_role = Role.objects.create(name='Admin', description='Administrator')
organizer_role = Role.objects.create(name='Organizer', description='Event Organizer')

# Create a test user
test_user = CustomUser.objects.create_user(
    email='student@farewell.local',
    password='test123',
    first_name='John',
    last_name='Doe',
    roles=[organizer_role]
)

# Create a timeline
timeline = Timeline.objects.create(
    title='Farewell Events 2024',
    description='Main farewell event timeline',
    published=True,
    category='events'
)

# Create timeline events
event = TimelineEvent.objects.create(
    timeline=timeline,
    title='Opening Ceremony',
    description='Official opening ceremony',
    scheduled_date='2024-02-15',
    location='Main Hall'
)

# Create responsibility categories
category = ResponsibilityCategory.objects.create(
    name='Decoration',
    description='Event decoration tasks'
)

# Create responsibilities
responsibility = Responsibility.objects.create(
    title='Setup decorations',
    description='Arrange all decorations for opening ceremony',
    category=category,
    assigned_to=test_user,
    priority='High',
    status='Pending',
    due_date='2024-02-14'
)
```

### 🧪 Running Tests

```bash
cd backend
"/home/alamin/Desktop/Others Projects/versity_farewell/.venv/bin/python" manage.py test users
```

### 🗄️ Database Access

View the SQLite database:
- File location: `backend/db.sqlite3`
- Access via admin panel or Django shell

### 📱 Next Steps (Phase 3)

The following needs to be implemented:

1. **API Views & ViewSets**
   - UserAuthViewSet (register, login, logout)
   - UserProfileViewSet (CRUD)
   - TimelineViewSet (CRUD)
   - ResponsibilityViewSet (CRUD)

2. **Permission Classes**
   - IsAuthenticated
   - IsOrganizer
   - IsTreasurer
   - IsAdmin

3. **URL Routing**
   - REST API endpoint configuration
   - Token endpoint for JWT

4. **API Documentation**
   - Swagger/OpenAPI documentation
   - API client examples

5. **Frontend Setup**
   - React 18 + TypeScript
   - Vite build system
   - React Query for state management
   - Axios for HTTP requests
   - Ant Design UI components

### 🐳 Docker Alternative

If you want to use Docker instead:

```bash
# Make sure Docker daemon is running
docker-compose up -d

# Access the application
# API: http://localhost
# Admin: http://localhost/admin
# PostgreSQL: localhost:5432
# Redis: localhost:6379
```

### 🔍 Troubleshooting

**Server won't start?**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill any existing Django process
pkill -f "python manage.py runserver"
```

**Database issues?**
```bash
# Reset database
rm backend/db.sqlite3

# Re-run migrations
cd backend && "/home/alamin/Desktop/Others Projects/versity_farewell/.venv/bin/python" manage.py migrate
```

**Module not found errors?**
```bash
# Reinstall dependencies
"/home/alamin/Desktop/Others Projects/versity_farewell/.venv/bin/python" -m pip install -r backend/requirements.txt
```

### 📚 Project Structure Review

```
versity_farewell/
├── backend/
│   ├── config/              # Django settings & WSGI
│   ├── users/              # User authentication app
│   │   ├── models.py       # CustomUser, UserProfile, Role
│   │   ├── serializers.py  # REST serializers
│   │   ├── admin.py        # Admin interface
│   │   └── tests.py        # 8/8 passing tests
│   ├── timeline/           # Timeline management app
│   │   ├── models.py       # Timeline, TimelineEvent
│   │   └── admin.py        # Admin interface
│   ├── responsibilities/   # Task management app
│   │   ├── models.py       # Responsibility, Category, Role
│   │   └── admin.py        # Admin interface
│   ├── manage.py           # Django management
│   └── requirements.txt    # 17 dependencies
│
├── frontend_fw/            # React frontend (Phase 3)
│
├── docker-compose.yml      # Multi-service orchestration
├── Dockerfile.backend      # Backend containerization
├── nginx.conf             # Reverse proxy config
├── setup-local.sh         # Automated setup script
└── DOCKER_SETUP.md        # Docker documentation
```

### 🔐 Security Notes

- Development server is NOT suitable for production
- Credentials are development-only and should be changed
- DATABASE_URL auto-detection supports PostgreSQL for production
- CORS is configured for frontend domain
- CSRF protection is enabled
- JWT tokens expire after 5 minutes (access) / 1 day (refresh)

---

**Happy testing! 🎉**

When ready, proceed to Phase 3: API Endpoint Development
