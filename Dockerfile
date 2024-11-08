# Используем базовый образ с Python 3.11
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем необходимые пакеты, включая Redis
RUN apt-get update && \
    apt-get install -y redis-server && \
    rm -rf /var/lib/apt/lists/*

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Копируем .env файл с переменными окружения
COPY .env .env

# Запускаем Redis-сервер в фоновом режиме и запускаем приложение
CMD redis-server --daemonize yes && python3 main.py
