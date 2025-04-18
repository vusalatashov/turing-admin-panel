# Dockerfile
FROM python:3.12-slim

# Əsas asılılıqları quraşdır
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# İşçi kataloqu
WORKDIR /app

# requirements.txt faylını kopyala və asılılıqları quraşdır
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Layihəni kopyala
COPY . .

# Migrationları işlətmək və superuser yaratmaq (interaktiv olmadan)
CMD ["sh", "-c", "python manage.py migrate && echo 'from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\"turing\", \"turingacademyaz@gmail.com\", \"turingdev\")' | python manage.py shell && python manage.py runserver 0.0.0.0:8080"]
