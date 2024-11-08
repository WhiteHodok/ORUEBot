# Используем базовый образ с Python 3.11
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Копируем .env файл с переменными окружения
COPY .env .env

# Указываем команду для запуска приложения
CMD ["python3", "main.py"]
