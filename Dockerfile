# Базовый образ с Python
FROM python:3

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы в контейнер
COPY ./app ./app
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду для запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
