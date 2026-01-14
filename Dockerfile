# Build frontend
FROM node:20-alpine as frontend-build

WORKDIR /app/frontend
COPY frontend_fw/package*.json ./
COPY frontend_fw/yarn.lock ./
RUN yarn install --frozen-lockfile
COPY frontend_fw/ .
RUN yarn build

# Build backend
FROM python:3.10-slim as backend-build

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app/backend
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY backend/ .

# Final image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    supervisor \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY --from=backend-build /app/backend /app/backend
WORKDIR /app/backend

# Install Python dependencies in final stage
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy frontend build
COPY --from=frontend-build /app/frontend/dist /usr/share/nginx/html

# Copy configs
COPY nginx.conf /etc/nginx/nginx.conf
COPY supervisord.conf /etc/supervisord.conf

# Create directories for logs
RUN mkdir -p /var/log/supervisor /var/log/nginx /var/log/gunicorn

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app /usr/share/nginx /var/log/supervisor /var/log/nginx /var/log/gunicorn /var/run

# Expose port
EXPOSE 80

# Set environment variables
ENV DEBUG=False \
    SECRET_KEY=django-production-secret-key-change-this \
    ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0 \
    CORS_ALLOWED_ORIGINS=http://localhost,http://127.0.0.1 \
    USE_REDIS=False

# Run migrations and collect static, then start supervisord
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    supervisord -c /etc/supervisord.conf
