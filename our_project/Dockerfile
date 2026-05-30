# Базовый образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости для PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt
# Копируем весь код проекта
COPY . .

# !!! СТРОКУ С COLLECTSTATIC МЫ УДАЛИЛИ ОТСЮДА !!!

# Открываем порт
EXPOSE 8000

# Команда запуска (daphne для веб-сокетов)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "our_project.asgi:application"]
