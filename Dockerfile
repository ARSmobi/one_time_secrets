FROM python:3.11-slim

# Установка зависимостей
WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходников
COPY . .

# Команда запуска (необязательна — у нас она уже прописана в docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
