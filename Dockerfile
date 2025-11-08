# Dockerfile для AI Business Intelligence Agent

FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости для PyMuPDF, pydub и других библиотек
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем директорию для загрузок
RUN mkdir -p downloads

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Порт не нужен для Telegram бота, но можно добавить для мониторинга
# EXPOSE 8000

# Команда запуска бота
CMD ["python", "main.py"]
