FROM python:3.10-slim

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app/backend

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files at build time
RUN python manage.py collectstatic --noinput

# Expose backend port
EXPOSE 8000

# Run with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "config.wsgi:application"]
