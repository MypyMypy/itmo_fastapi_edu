# Glossary API

## Функциональность

- Получение списка терминов
- Добавление нового термина
- Обновление существующего термина
- Удаление термина

### Локальный запуск

1. Клонируйте репозиторий:

   ```bash
   git clone <URL репозитория>
   cd repository

   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Запустите сервер: `uvicorn app.main:app --reload`

4. Откройте в браузере:

- Swagger UI: http://127.0.0.1:8000/docs

- ReDoc: http://127.0.0.1:8000/redoc

## Запуск в Docker

1. `docker compose up --build`

Откройте API по адресу http://localhost:8000.
