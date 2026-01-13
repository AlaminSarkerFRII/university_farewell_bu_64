# Redis Connection Fix

## Problem
Django admin login was failing with error:
```
ConnectionError: Error 111 connecting to 127.0.0.1:6379. Connection refused.
```

This occurred because:
- Django was configured to use Redis for caching and sessions
- Redis server was not installed/running on the local machine
- The application couldn't start sessions without Redis connection

## Solution Applied

Updated `backend/config/settings.py` to use **fallback caching** that works without Redis:

### Changes Made:

1. **Made Redis optional**: Added `USE_REDIS` environment variable
2. **Fallback caching**: When Redis is unavailable, use Django's built-in `LocMemCache`
3. **Fallback sessions**: When Redis is unavailable, use database-backed sessions

### Configuration:

```python
# For local development (without Redis):
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# For production (with Redis):
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        ...
    }
}
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
```

## How to Use

### Option 1: Run WITHOUT Redis (Default - Recommended for Local Development)

Just run your Django server normally:
```bash
cd backend
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
python manage.py runserver
```

The app will automatically use local memory cache and database sessions.

### Option 2: Run WITH Redis (For Production or Testing)

If you want to use Redis, you need to:

**Step 1: Install Redis**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server

# macOS
brew install redis

# Windows
# Download from: https://redis.io/download
```

**Step 2: Start Redis**
```bash
# Ubuntu/Debian
sudo systemctl start redis-server
sudo systemctl enable redis-server

# macOS
brew services start redis

# Or run in foreground
redis-server
```

**Step 3: Set environment variable**
Create/update your `.env` file:
```env
USE_REDIS=True
REDIS_URL=redis://127.0.0.1:6379/0
```

**Step 4: Verify Redis is running**
```bash
redis-cli ping
# Should return: PONG
```

## Testing the Fix

1. **Stop any running Django server** (Ctrl+C)

2. **Restart the Django server**:
```bash
cd backend
python manage.py runserver
```

3. **Test admin login**:
- Open browser: http://127.0.0.1:8000/admin/
- Login with your admin credentials
- Should work without Redis connection errors!

## Understanding the Difference

### Local Memory Cache (Default):
- ✅ No installation required
- ✅ Works immediately
- ⚠️ Cache is per-process (not shared between workers)
- ⚠️ Cache is cleared when server restarts

### Redis Cache (Optional):
- ✅ Shared cache across multiple workers
- ✅ Persistent cache (survives restarts)
- ✅ Better performance for production
- ⚠️ Requires Redis installation and maintenance

## Troubleshooting

### Still getting connection errors?
1. Make sure you stopped and restarted the Django server after the fix
2. Check that no `.env` file has `USE_REDIS=True` set
3. Clear browser cookies and try again

### Want to verify sessions are working?
```bash
# Check session table exists
python manage.py migrate

# List sessions in database
python manage.py shell
>>> from django.contrib.sessions.models import Session
>>> print(Session.objects.count())
```

## For Docker Deployment

When using Docker, Redis is included in `docker-compose.yml`. Set these in `.env.docker`:
```env
USE_REDIS=True
REDIS_URL=redis://redis:6379/0
```

Redis will automatically start as part of the Docker stack.
