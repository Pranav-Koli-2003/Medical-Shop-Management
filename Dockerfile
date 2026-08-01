# Dockerfile — Medical Shop Management System
# Builds a production-style image for the Django app.

FROM python:3.12-slim

# Prevents Python from writing .pyc files and buffers stdout (cleaner container logs)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (separate layer = faster rebuilds when only code changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project
COPY . .

# Collect static files (CSS/JS/Images) into one folder for production serving
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Run with Gunicorn instead of the dev server — this is what makes it "production-style"
CMD ["gunicorn", "Medical_Shop.wsgi:application", "--bind", "0.0.0.0:8000"]
