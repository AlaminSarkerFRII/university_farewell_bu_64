# 🔍 Swagger/OpenAPI API Documentation Setup

**Status**: ✅ COMPLETE - Swagger Now Enabled!

---

## 🌐 Swagger/Redoc URLs

Once you start the Django server, access API documentation at:

### 🎯 **Primary Documentation URL** (Most Popular)
```
http://localhost:8000/api/docs/
```
**Interface**: Swagger UI  
**Features**: Interactive testing, authorization, request/response examples  
**Best for**: Quick testing and exploration

### 📚 **Alternative Documentation URL**
```
http://localhost:8000/api/redoc/
```
**Interface**: ReDoc  
**Features**: Beautiful, organized documentation  
**Best for**: Reading and sharing documentation

### 📋 **Raw OpenAPI Schema**
```
http://localhost:8000/api/schema/
```
**Format**: JSON OpenAPI 3.0 Schema  
**Best for**: Importing into other tools (Postman, Insomnia, etc.)

---

## 🚀 Quick Start

### 1. Start Django Server
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

### 2. Open Swagger in Browser
```
http://localhost:8000/api/docs/
```

### 3. Test an Endpoint
1. Click on any endpoint (e.g., `POST /api/auth/login/`)
2. Click "Try it out"
3. Fill in request data
4. Click "Execute"
5. See response below

---

## 📖 Using Swagger UI

### Login to Get Auth Token

1. **Navigate to**: `http://localhost:8000/api/docs/`
2. **Find**: `POST /api/auth/login/`
3. **Click**: "Try it out"
4. **Enter**:
   ```json
   {
     "email": "admin@farewell.local",
     "password": "admin123"
   }
   ```
5. **Click**: "Execute"
6. **Copy**: The `access` token from response

### Authorize for Protected Endpoints

1. **Click** the green "Authorize" button at top-right
2. **Select**: "Bearer" or "HTTPBearer"
3. **Enter**: `Bearer {your_access_token}`
4. **Click**: "Authorize"
5. **Click**: "Close"

Now all authenticated endpoints will use your token automatically!

---

## 🔌 API Endpoints in Swagger

### Authentication Endpoints
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login and get token
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/refresh_token/` - Refresh access token

### User Endpoints
- `GET /api/users/` - List all users (admin)
- `POST /api/users/` - Create user (admin)
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `GET /api/users/profile/` - Get current user profile
- `PUT /api/users/update_profile/` - Update profile
- `POST /api/users/change_password/` - Change password

### Timeline Endpoints
- `GET /api/timelines/` - List timelines
- `POST /api/timelines/` - Create timeline
- `GET /api/timelines/{id}/` - Get timeline
- `PATCH /api/timelines/{id}/` - Update timeline
- `DELETE /api/timelines/{id}/` - Delete timeline
- `POST /api/timelines/{id}/publish/` - Publish timeline
- `POST /api/timelines/{id}/unpublish/` - Unpublish timeline
- `POST /api/timelines/{id}/feature/` - Feature timeline
- `GET /api/timelines/{id}/events/` - Get timeline events

### Timeline Events Endpoints
- `GET /api/timeline-events/` - List events
- `POST /api/timeline-events/` - Create event
- `GET /api/timeline-events/{id}/` - Get event
- `PATCH /api/timeline-events/{id}/` - Update event

### Responsibility Endpoints
- `GET /api/responsibilities/` - List responsibilities
- `POST /api/responsibilities/` - Create responsibility
- `GET /api/responsibilities/{id}/` - Get responsibility
- `PATCH /api/responsibilities/{id}/update_status/` - Update status
- `POST /api/responsibilities/{id}/assign_to/` - Assign to user
- `GET /api/responsibilities/my_responsibilities/` - Get own tasks
- `GET /api/responsibilities/by_status/` - Group by status
- `GET /api/responsibilities/by_priority/` - Group by priority

### Category Endpoints
- `GET /api/responsibility-categories/` - List categories
- `POST /api/responsibility-categories/` - Create category
- `GET /api/responsibility-categories/{id}/` - Get category
- `PATCH /api/responsibility-categories/{id}/` - Update category

---

## 🎓 Example: Testing Login Endpoint

### In Swagger UI:

1. **Go to**: http://localhost:8000/api/docs/
2. **Search for**: "login"
3. **Click**: `POST /api/auth/login/`
4. **Click**: "Try it out"
5. **Request Body**:
   ```json
   {
     "email": "admin@farewell.local",
     "password": "admin123"
   }
   ```
6. **Click**: "Execute"

### Response (Success):
```json
{
  "message": "Login successful",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "admin@farewell.local",
    "first_name": "Admin",
    "role": "admin",
    "is_active": true
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

## 🔐 Authorization in Swagger

### Method 1: Bearer Token (Recommended)

1. **Get token** from login endpoint
2. **Click** "Authorize" button (top-right green button)
3. **Select** "Bearer"
4. **Paste**: `eyJ0eXAi...` (access token)
5. **Click** "Authorize"

Now all requests include: `Authorization: Bearer {token}`

### Method 2: Manual Header

Some endpoints allow you to manually add headers:

1. **In request section**, find "Headers"
2. **Add header**: 
   ```
   Key: Authorization
   Value: Bearer {your_token}
   ```

---

## 📊 Testing Filtered Endpoints

### Example: Filter Timelines

1. **Go to**: `GET /api/timelines/`
2. **Click**: "Try it out"
3. **Query Parameters**:
   - `category`: `events`
   - `is_published`: `true`
   - `search`: `ceremony`
   - `ordering`: `-created_at`
4. **Click**: "Execute"

---

## 🛠️ Importing OpenAPI Schema to Postman

### Step 1: Get Schema URL
```
http://localhost:8000/api/schema/
```

### Step 2: In Postman
1. Click "Collections" → "Import"
2. Select "Link" tab
3. Paste: `http://localhost:8000/api/schema/`
4. Click "Continue"
5. Click "Import"

Now Postman has all your API endpoints pre-configured!

---

## 📁 File Structure

### Swagger Setup Files
```
backend/
├── config/
│   ├── settings.py (Updated with drf_spectacular)
│   └── urls.py (Updated with Swagger routes)
├── users/
│   └── views.py (ViewSets)
├── timeline/
│   └── views.py (ViewSets)
├── responsibilities/
│   └── views.py (ViewSets)
└── requirements.txt (Added drf-spectacular)
```

### Removed Files
- ~~users/viewsets.py~~ → Moved to users/views.py
- ~~timeline/viewsets.py~~ → Moved to timeline/views.py
- ~~responsibilities/viewsets.py~~ → Moved to responsibilities/views.py

---

## ⚙️ Configuration Details

### Settings Added (config/settings.py)

```python
# Added to INSTALLED_APPS
'drf_spectacular',

# Added to REST_FRAMEWORK
'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

# New configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'Versity Farewell API',
    'DESCRIPTION': 'REST API for Event Management and Responsibility Tracking',
    'VERSION': '1.0.0',
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
}
```

### URLs Added (config/urls.py)

```python
# Swagger/OpenAPI Documentation
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
```

---

## 🔍 Advanced Swagger Features

### Download OpenAPI Spec
- Click download button in Swagger UI
- Save as `openapi.json`

### Share Documentation
- Copy: `http://localhost:8000/api/docs/`
- Share with team
- Everyone can test endpoints

### Use with Frontend
```javascript
// React example
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';
const token = localStorage.getItem('access_token');

axios.get(`${API_URL}/timelines/`, {
  headers: { Authorization: `Bearer ${token}` }
});
```

---

## 🐛 Troubleshooting

### Issue: Swagger not showing
**Solution**: Restart server and clear cache
```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Restart server
python manage.py runserver 0.0.0.0:8000
```

### Issue: Can't authorize
**Solution**: 
1. Login first to get token
2. Make sure token has `Bearer ` prefix
3. Check token hasn't expired

### Issue: Some endpoints not showing
**Solution**: 
1. Check endpoint has docstring
2. Verify permissions are correct
3. Restart server

---

## 📚 Swagger Features You Can Use

### 1. **Try it out** - Test endpoints directly
### 2. **Authorize** - Add JWT tokens
### 3. **Parameters** - Set query/path params
### 4. **Response** - See actual responses
### 5. **Headers** - View all headers
### 6. **Download** - Export OpenAPI schema
### 7. **Share** - Send documentation link

---

## 🎯 Complete Workflow

```
1. Start Server
   ↓
2. Open http://localhost:8000/api/docs/
   ↓
3. Find POST /api/auth/login/
   ↓
4. Click "Try it out"
   ↓
5. Enter email & password
   ↓
6. Execute
   ↓
7. Copy access token
   ↓
8. Click Authorize button
   ↓
9. Paste token with "Bearer " prefix
   ↓
10. Now test all endpoints!
```

---

## ✅ Verification

Swagger is working if you see:

1. ✅ Page loads at `http://localhost:8000/api/docs/`
2. ✅ All endpoints listed on left side
3. ✅ Can login and get token
4. ✅ Authorization header works
5. ✅ Can execute test requests
6. ✅ See responses below each request

---

## 🚀 Next Steps

1. **Test all 40+ endpoints** using Swagger
2. **Verify permissions** are working correctly
3. **Test filtering** on list endpoints
4. **Import schema** to Postman/Insomnia
5. **Share documentation** with frontend team
6. **Start frontend** development

---

## 📞 Quick Links

| Resource | URL |
|----------|-----|
| Swagger UI | http://localhost:8000/api/docs/ |
| ReDoc | http://localhost:8000/api/redoc/ |
| OpenAPI Schema | http://localhost:8000/api/schema/ |
| Admin Panel | http://localhost:8000/admin/ |
| GitHub Repo | https://github.com/AlaminSarkerFRII/university_farewell_bu_64 |

---

## ✨ What's Fixed

✅ Moved all ViewSet code from `viewsets.py` to `views.py`  
✅ Installed `drf-spectacular` for Swagger  
✅ Configured Swagger/OpenAPI documentation  
✅ Added 3 documentation endpoints (Swagger, ReDoc, Schema)  
✅ Verified system check (0 issues)  
✅ Ready to test all APIs!

---

**Swagger is now active!** 🎉

Go to **http://localhost:8000/api/docs/** to see your API documentation!

