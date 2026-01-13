# Docker Setup Guide

## Prerequisites
- Docker Desktop installed ([Download](https://www.docker.com/products/docker-desktop))
- Docker Compose installed (included with Docker Desktop)
- Git configured

## Quick Start with Docker

### 1. Clone and Setup
```bash
git clone https://github.com/AlaminSarkerFRII/university_farewell_bu_64.git
cd university_farewell_bu_64
```

### 2. Start Services
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
```

### 3. Create Superuser (first time only)
```bash
docker-compose exec backend python manage.py createsuperuser
```

### 4. Access Services

| Service | URL | Purpose |
|---------|-----|---------|
| **Django Admin** | http://localhost/admin | Admin dashboard |
| **API Root** | http://localhost/api | API endpoints |
| **Health Check** | http://localhost/health | Server status |

### 5. Run Migrations
```bash
# Manually run migrations (if needed)
docker-compose exec backend python manage.py migrate
```

### 6. Collect Static Files
```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

---

## Common Docker Commands

### Useful Commands
```bash
# View all containers
docker-compose ps

# View logs
docker-compose logs backend       # Backend logs
docker-compose logs db            # Database logs
docker-compose logs nginx         # Nginx logs

# Stop all services
docker-compose down

# Stop with volume cleanup
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# Access backend shell
docker-compose exec backend bash

# Run Django management commands
docker-compose exec backend python manage.py shell
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

### Database Management
```bash
# Access PostgreSQL CLI
docker-compose exec db psql -U farewell_user -d versity_farewell

# Backup database
docker-compose exec db pg_dump -U farewell_user versity_farewell > backup.sql

# Restore database
docker-compose exec -T db psql -U farewell_user versity_farewell < backup.sql
```

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│            DOCKER COMPOSE NETWORK                   │
├─────────────────────────────────────────────────────┤
│                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │
│  │   Nginx      │  │   Backend    │  │ Database │  │
│  │   (Port 80)  │  │  (Port 8000) │  │(Port 5432)│  │
│  └──────────────┘  └──────────────┘  └──────────┘  │
│         │                  │                │        │
│         └──────────────────┼────────────────┘        │
│                            │                         │
│                    ┌──────────────┐                  │
│                    │   Redis      │                  │
│                    │ (Port 6379)  │                  │
│                    └──────────────┘                  │
│                                                       │
└─────────────────────────────────────────────────────┘
     ↓
   Localhost (Browser/API Client)
```

---

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port
lsof -i :80          # Find process on port 80
kill -9 <PID>        # Kill the process

# Or change ports in docker-compose.yml
```

### Database Connection Error
```bash
# Check database logs
docker-compose logs db

# Restart database
docker-compose restart db

# Check database health
docker-compose exec db pg_isready -U farewell_user
```

### Container Won't Start
```bash
# View error logs
docker-compose logs backend

# Rebuild image
docker-compose build --no-cache backend
docker-compose up -d backend
```

### Clear All Data
```bash
# Stop and remove everything including volumes
docker-compose down -v

# Restart fresh
docker-compose up -d
```

---

## Environment Variables

Edit `.env.docker` to customize:
- `DEBUG` - Enable/disable debug mode
- `DATABASE_URL` - Database connection string
- `REDIS_URL` - Redis connection
- `CORS_ALLOWED_ORIGINS` - CORS settings
- `ALLOWED_HOSTS` - Allowed hostnames

---

## Performance Tips

1. **Increase Docker Memory** if experiencing slowness
   - Docker Desktop Settings → Resources → Memory (set to 4GB+)

2. **Use .dockerignore** to exclude unnecessary files

3. **Enable BuildKit** for faster builds
   ```bash
   export DOCKER_BUILDKIT=1
   docker-compose build --no-cache
   ```

4. **Monitor Resources**
   ```bash
   docker stats
   ```

---

## Production Deployment

For production:
1. Update `SECRET_KEY` in `.env`
2. Set `DEBUG=False`
3. Use stronger database credentials
4. Configure proper email backend
5. Setup HTTPS/SSL certificates
6. Use separate container registry
7. Enable health checks
8. Setup log aggregation

See `DEPLOYMENT.md` for detailed instructions.

---

**Last Updated**: January 13, 2026  
**Created for**: Local Development & Testing
