# Telegram Mini App Backend (FastAPI)

Минимальный backend-микросервис для Telegram Mini Apps, готовый к деплою на Render.

## Возможности

- `GET /` — healthcheck
- `GET /webapp` — входная точка Telegram Mini App
- Валидация `initData` от Telegram (hash-подпись через `BOT_TOKEN`)
- Парсинг пользователя: `id`, `username`, `language_code`
- JSON-only API (без HTML и UI)

## Структура

```text
app/
 ├── main.py
 ├── config.py
 ├── routers/
 │    └── webapp.py
 ├── services/
 │    └── telegram.py
 ├── models/
 │    └── user.py
 ├── requirements.txt
 └── README.md
```

## Локальный запуск

1. Установить Python 3.11.
2. Создать и активировать виртуальное окружение.
3. Установить зависимости:

   ```bash
   pip install -r app/requirements.txt
   ```

4. Установить переменную окружения с токеном бота:

   ```bash
   export BOT_TOKEN="<YOUR_TELEGRAM_BOT_TOKEN>"
   ```

5. Запустить сервер:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 10000
   ```

6. Проверить:
   - `GET http://localhost:10000/`
   - `GET http://localhost:10000/webapp` (с `X-Telegram-Init-Data` или `initData`)

## Деплой на Render

1. Создать новый **Web Service** из вашего Git-репозитория.
2. Указать окружение Python 3.11.
3. Build Command:

   ```bash
   pip install -r app/requirements.txt
   ```

4. Start Command:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 10000
   ```

5. В Environment Variables добавить:
   - `BOT_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>`

После деплоя endpoint будет доступен по URL Render-сервиса.

## Подключение Mini App к Telegram-боту

1. Создайте бота через `@BotFather` и получите `BOT_TOKEN`.
2. Задайте Web App URL (URL вашего Render-сервиса) для кнопки/меню бота.
3. В Mini App Telegram передавайте `initData` на backend:
   - заголовком `X-Telegram-Init-Data`
   - или query-параметром `initData`
4. Backend проверяет подпись `hash` и возвращает JSON с данными пользователя.

## Пример ответа `GET /webapp`

```json
{
  "ok": true,
  "user": {
    "id": 123456789,
    "username": "my_username",
    "language_code": "ru"
  }
}
```
