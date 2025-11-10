# 🛠️ Команды для работы с проектом

> **AI Business Assistant** - Полное руководство по командам
> **Версия:** 2.0 (Gemini 1.5 Pro)

---

## 📋 Содержание

1. [Первоначальная установка](#первоначальная-установка)
2. [Запуск проекта](#запуск-проекта)
3. [Отладка и диагностика](#отладка-и-диагностика)
4. [Тестирование](#тестирование)
5. [Работа с базой данных](#работа-с-базой-данных)
6. [Веб-приложение](#веб-приложение)
7. [Docker](#docker)
8. [Production deployment](#production-deployment)
9. [Полезные утилиты](#полезные-утилиты)

---

## 🔧 Первоначальная установка

### 1. Клонирование и настройка

```bash
# Клонировать репозиторий
git clone https://github.com/kandibobe/ai-business-asistant.git
cd ai-business-asistant

# Создать виртуальное окружение
python -m venv .venv

# Активировать виртуальное окружение
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Установить зависимости
pip install --upgrade pip
pip install -r requirements.txt

# Скопировать .env файл
cp .env.example .env

# Открыть .env в редакторе и заполнить ключи
nano .env  # или vim, code, notepad++
```

### 2. Проверка установки

```bash
# Проверить Python версию
python --version  # Должно быть 3.10+

# Проверить установленные пакеты
pip list | grep -E "(telegram|gemini|postgres|redis|celery)"

# Проверить настройку проекта
python check_setup.py

# Проверить зависимости
python check_dependencies.py
```

### 3. Установка системных зависимостей

```bash
# Linux (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y ffmpeg libmagic1 postgresql-client redis-tools

# Mac
brew install ffmpeg libmagic postgresql redis

# Windows (через chocolatey)
choco install ffmpeg
# python-magic-bin устанавливается через pip автоматически
```

---

## 🚀 Запуск проекта

### Вариант 1: Быстрый старт (все в одном)

```bash
# Windows - автоматический запуск всего
start_bot.bat

# Linux/Mac - ручной запуск каждого компонента
# Терминал 1: PostgreSQL + Redis (если Docker)
docker-compose up -d

# Терминал 2: Celery Worker
celery -A celery_app worker --loglevel=info

# Терминал 3: Telegram Bot
python main.py

# Терминал 4: Web API (опционально)
cd api
uvicorn main:app --reload --port 8000
```

### Вариант 2: Пошаговый запуск

#### Шаг 1: Запустить инфраструктуру

```bash
# Docker Compose (PostgreSQL + Redis)
docker-compose up -d

# Проверить статус
docker-compose ps

# Посмотреть логи
docker-compose logs -f

# Остановить
docker-compose down
```

#### Шаг 2: Инициализировать базу данных

```bash
# Применить миграции
python migrate_db.py

# Или создать с нуля
python -c "
from database.database import init_db
init_db()
print('✅ Database initialized')
"

# Проверить подключение к БД
python -c "
from database.database import SessionLocal
db = SessionLocal()
print('✅ Database connection OK')
db.close()
"
```

#### Шаг 3: Запустить Celery Worker

```bash
# Linux/Mac
celery -A celery_app worker --loglevel=info

# Windows (обязательно с --pool=solo)
celery -A celery_app worker --loglevel=info --pool=solo

# Или используйте готовый скрипт
# Windows:
start_worker.bat

# Проверить задачи Celery
celery -A celery_app inspect active
celery -A celery_app inspect registered

# Посмотреть статистику
celery -A celery_app inspect stats
```

#### Шаг 4: Запустить Telegram бота

```bash
# Обычный запуск
python main.py

# С повышенным логированием
LOG_LEVEL=DEBUG python main.py

# В фоновом режиме (Linux/Mac)
nohup python main.py > bot.log 2>&1 &

# Проверить, что бот запущен
ps aux | grep main.py
```

#### Шаг 5: Запустить Web API (опционально)

```bash
# Development mode с auto-reload
uvicorn api.main:app --reload --port 8000

# Production mode
uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4

# С SSL (production)
uvicorn api.main:app --host 0.0.0.0 --port 8000 --ssl-keyfile=key.pem --ssl-certfile=cert.pem

# Проверить API
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger UI
```

---

## 🐛 Отладка и диагностика

### Проверка конфигурации

```bash
# Проверить .env переменные
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('TELEGRAM_BOT_TOKEN:', os.getenv('TELEGRAM_BOT_TOKEN')[:10] + '...' if os.getenv('TELEGRAM_BOT_TOKEN') else 'NOT SET')
print('GEMINI_API_KEY:', os.getenv('GEMINI_API_KEY')[:10] + '...' if os.getenv('GEMINI_API_KEY') else 'NOT SET')
print('DB_HOST:', os.getenv('DB_HOST'))
print('REDIS_URL:', os.getenv('REDIS_URL'))
"

# Проверить модель Gemini
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-pro-002')
response = model.generate_content('Hello!')
print('✅ Gemini 1.5 Pro working!')
print('Response:', response.text[:100])
"
```

### Проверка подключений

```bash
# Проверить PostgreSQL
psql -h localhost -U ai_bot_user -d ai_bot_db -c "SELECT version();"

# Проверить Redis
redis-cli ping

# Проверить подключение из Python
python -c "
import redis
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# Redis
r = redis.from_url(os.getenv('REDIS_URL'))
print('✅ Redis:', r.ping())

# PostgreSQL
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    database=os.getenv('DB_NAME')
)
print('✅ PostgreSQL: Connected')
conn.close()
"
```

### Просмотр логов

```bash
# Логи Docker контейнеров
docker-compose logs -f postgres
docker-compose logs -f redis

# Логи бота (если запущен в фоне)
tail -f bot.log

# Логи Celery
tail -f celery.log

# Логи с фильтрацией по уровню
grep "ERROR" bot.log
grep "WARNING" celery.log

# Реальное время с выделением ошибок
tail -f bot.log | grep --color=always -E "ERROR|WARNING|$"
```

### Диагностика проблем

```bash
# Проверить открытые порты
netstat -tuln | grep -E "(5432|6379|8000)"

# Linux
ss -tuln | grep -E "(5432|6379|8000)"

# Проверить процессы
ps aux | grep python
ps aux | grep celery

# Убить зависший процесс
# Найти PID
ps aux | grep main.py
# Убить
kill -9 <PID>

# Очистить Redis (ОСТОРОЖНО!)
redis-cli FLUSHALL

# Очистить очередь Celery
celery -A celery_app purge

# Пересоздать БД (УДАЛИТ ВСЕ ДАННЫЕ!)
python -c "
from database.database import engine, Base
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print('✅ Database recreated')
"
```

---

## 🧪 Тестирование

### Установка тестовых зависимостей

```bash
# Установить pytest и плагины
pip install pytest pytest-asyncio pytest-cov pytest-mock faker

# Проверить установку
pytest --version
```

### Запуск тестов

```bash
# Запустить все тесты
pytest

# С подробным выводом
pytest -v

# С выводом print statements
pytest -s

# Запустить конкретный файл
pytest tests/unit/test_security.py

# Запустить конкретный тест
pytest tests/unit/test_security.py::TestFileValidation::test_valid_pdf_file

# Запустить по паттерну
pytest -k "test_security"

# Параллельный запуск (быстрее)
pip install pytest-xdist
pytest -n auto
```

### Тестирование с покрытием

```bash
# Coverage report
pytest --cov=. --cov-report=term-missing

# HTML отчет
pytest --cov=. --cov-report=html
# Открыть htmlcov/index.html в браузере

# XML отчет (для CI/CD)
pytest --cov=. --cov-report=xml

# Только unit тесты
pytest tests/unit/ --cov=. --cov-report=term

# Только integration тесты
pytest tests/integration/ --cov=. --cov-report=term
```

### Тестирование отдельных компонентов

```bash
# Тест безопасности
pytest tests/unit/test_security.py -v

# Тест валидаторов
pytest tests/unit/test_validators.py -v

# Тест AI helpers
pytest tests/unit/test_ai_helpers.py -v

# Тест file validators
pytest tests/unit/test_file_validators.py -v

# Тест rate limiter
pytest tests/unit/test_rate_limiter.py -v

# Тест моделей БД
pytest tests/unit/test_models.py -v

# Тест CRUD операций
pytest tests/unit/test_crud.py -v
```

### Мануальное тестирование

```bash
# Тест security модуля
python -c "
from utils.security import validate_file, sanitize_text_input, validate_url

# Тест валидации файла
is_valid, msg = validate_file('test.pdf', 'test.pdf', 'pdf')
print(f'File validation: {is_valid}')

# Тест санитизации
try:
    clean = sanitize_text_input('SELECT * FROM users; DROP TABLE users;')
    print('Should have raised SecurityError!')
except Exception as e:
    print(f'✅ Security check passed: {e}')

# Тест URL
is_valid, msg = validate_url('https://example.com')
print(f'URL validation: {is_valid}')
"

# Тест rate limiter
python -c "
from middleware.rate_limiter import check_rate_limit, get_rate_limit_info

user_id = 12345
action = 'ai_requests'

# Проверить текущий статус
info = get_rate_limit_info(user_id, action)
print(f'Rate limit info: {info}')

# Тест лимита
for i in range(10):
    try:
        check_rate_limit(user_id, action)
        print(f'Request {i+1}: OK')
    except Exception as e:
        print(f'Request {i+1}: BLOCKED - {e}')
        break
"

# Тест AI helpers
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv
from utils.ai_helpers import generate_ai_response

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-pro-002')

# Тест с кэшированием
response1 = generate_ai_response(
    model=model,
    prompt='What is 2+2?',
    use_cache=True
)
print(f'Response: {response1[\"message\"]}')
print(f'Cached: {response1[\"cached\"]}')
print(f'Time: {response1[\"response_time_ms\"]}ms')

# Второй запрос (должен быть из кэша)
response2 = generate_ai_response(
    model=model,
    prompt='What is 2+2?',
    use_cache=True
)
print(f'Second request cached: {response2[\"cached\"]}')
"
```

---

## 💾 Работа с базой данных

### Миграции

```bash
# Применить миграции
python migrate_db.py

# Создать новую миграцию
alembic revision --autogenerate -m "Add new field"

# Применить все миграции
alembic upgrade head

# Откатить на одну миграцию назад
alembic downgrade -1

# Посмотреть текущую версию
alembic current

# История миграций
alembic history
```

### Backup и Restore

```bash
# Backup базы данных
pg_dump -h localhost -U ai_bot_user ai_bot_db > backup.sql

# Restore
psql -h localhost -U ai_bot_user ai_bot_db < backup.sql

# Backup с сжатием
pg_dump -h localhost -U ai_bot_user ai_bot_db | gzip > backup.sql.gz

# Restore из сжатого
gunzip -c backup.sql.gz | psql -h localhost -U ai_bot_user ai_bot_db
```

### Прямой доступ к БД

```bash
# Подключиться к БД
psql -h localhost -U ai_bot_user -d ai_bot_db

# В psql:
# Посмотреть все таблицы
\dt

# Описание таблицы
\d users
\d documents

# SQL запросы
SELECT * FROM users LIMIT 10;
SELECT * FROM documents WHERE user_id = 123;
SELECT COUNT(*) FROM users;

# Выход
\q
```

### Python скрипты для БД

```bash
# Посмотреть всех пользователей
python -c "
from database.database import SessionLocal
from database.models import User

db = SessionLocal()
users = db.query(User).all()
for user in users:
    print(f'User {user.user_id}: {user.username}')
db.close()
"

# Посмотреть документы пользователя
python -c "
from database.database import SessionLocal
from database.crud import get_user_documents

db = SessionLocal()
docs = get_user_documents(db, user_id=123)
for doc in docs:
    print(f'{doc.file_name}: {doc.char_count} chars')
db.close()
"

# Очистить все документы (ОСТОРОЖНО!)
python -c "
from database.database import SessionLocal
from database.models import Document

db = SessionLocal()
db.query(Document).delete()
db.commit()
print('All documents deleted')
db.close()
"
```

---

## 🌐 Веб-приложение

### Запуск React приложения

```bash
# Перейти в директорию
cd web-app

# Установить зависимости (первый раз)
npm install

# Development server
npm run dev
# Открыть http://localhost:5173

# Production build
npm run build

# Preview production build
npm run preview

# Lint
npm run lint

# Type check
npm run type-check
```

### Работа с API

```bash
# Запустить API сервер
uvicorn api.main:app --reload --port 8000

# Проверить эндпоинты
curl http://localhost:8000/health
curl http://localhost:8000/docs    # Swagger UI
curl http://localhost:8000/redoc   # ReDoc

# Тест аутентификации
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "TestPass123"
  }'

# Тест логина
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPass123"
  }'

# Запрос с токеном
TOKEN="your_jwt_token_here"
curl http://localhost:8000/api/documents \
  -H "Authorization: Bearer $TOKEN"
```

### Одновременный запуск (Full Stack)

```bash
# В одном терминале
docker-compose up -d && \
celery -A celery_app worker --loglevel=info --pool=solo &
python main.py &
uvicorn api.main:app --reload --port 8000 &
cd web-app && npm run dev

# Или создайте скрипт start_all.sh:
#!/bin/bash
docker-compose up -d
sleep 5
celery -A celery_app worker --loglevel=info &
python main.py &
cd api && uvicorn main:app --reload --port 8000 &
cd ../web-app && npm run dev

# Сделать исполняемым и запустить
chmod +x start_all.sh
./start_all.sh
```

---

## 🐳 Docker

### Development

```bash
# Запустить только инфраструктуру
docker-compose up -d

# Запустить всё (бот + worker + БД + Redis)
docker-compose --profile full up -d

# Посмотреть логи
docker-compose logs -f
docker-compose logs -f postgres
docker-compose logs -f redis

# Остановить
docker-compose down

# Остановить и удалить volumes (УДАЛИТ ДАННЫЕ!)
docker-compose down -v

# Пересобрать образы
docker-compose build
docker-compose up -d --build
```

### Production Docker

```bash
# Собрать production образ
docker build -f Dockerfile.cloudrun -t ai-bot:latest .

# Запустить локально
docker run -p 8080:8080 --env-file .env ai-bot:latest

# Push в Google Container Registry
docker tag ai-bot:latest gcr.io/YOUR_PROJECT_ID/ai-bot:latest
docker push gcr.io/YOUR_PROJECT_ID/ai-bot:latest

# Pull и запуск
docker pull gcr.io/YOUR_PROJECT_ID/ai-bot:latest
docker run -d -p 8080:8080 gcr.io/YOUR_PROJECT_ID/ai-bot:latest
```

---

## ☁️ Production Deployment

### Google Cloud Run

```bash
# Аутентификация
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Создать секреты
echo -n "your_telegram_token" | gcloud secrets create telegram-bot-token --data-file=-
echo -n "your_gemini_key" | gcloud secrets create gemini-api-key --data-file=-
echo -n "your_db_password" | gcloud secrets create db-password --data-file=-

# Build через Cloud Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ai-bot

# Deploy на Cloud Run
gcloud run deploy ai-business-bot \
  --image gcr.io/YOUR_PROJECT_ID/ai-bot \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1

# Или использовать конфигурацию
gcloud run services replace cloud-run.yaml

# Посмотреть логи
gcloud run logs read --service ai-business-bot --limit 50

# Посмотреть URL
gcloud run services describe ai-business-bot --format="value(status.url)"
```

### GitHub Actions (CI/CD)

```bash
# Настроить секреты в GitHub:
# Settings → Secrets and variables → Actions

# Добавить секреты:
# - GCP_PROJECT_ID
# - GCP_SA_KEY (JSON ключ service account)

# Push в main для автоматического деплоя
git push origin main

# Посмотреть статус в GitHub:
# Actions tab → Latest workflow run
```

---

## 🔧 Полезные утилиты

### Проверка здоровья системы

```bash
# Общая проверка
python -c "
from utils.health_check import check_system_health

health = check_system_health()
for component, status in health.items():
    print(f'{component}: {status}')
"

# Проверка моделей
python check_models.py

# Проверка зависимостей
python check_dependencies.py
```

### Очистка проекта

```bash
# Удалить __pycache__
find . -type d -name __pycache__ -exec rm -rf {} +

# Удалить .pyc файлы
find . -type f -name "*.pyc" -delete

# Удалить downloads
rm -rf downloads/*

# Удалить logs
rm -rf logs/*.log

# Полная очистка (скрипт)
python cleanup_project.py
```

### Мониторинг ресурсов

```bash
# Использование памяти Python процессом
python -c "
import psutil
import os

process = psutil.Process(os.getpid())
print(f'Memory: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"

# Мониторинг в реальном времени
watch -n 1 'ps aux | grep python'

# Использование Docker ресурсов
docker stats

# Размер БД
psql -h localhost -U ai_bot_user -d ai_bot_db -c "
SELECT pg_size_pretty(pg_database_size('ai_bot_db'));
"
```

### Rate Limit управление

```bash
# Проверить лимиты пользователя
python -c "
from middleware.rate_limiter import get_rate_limit_info

info = get_rate_limit_info(user_id=123, action='ai_requests')
print(info)
"

# Сбросить лимит
python -c "
from middleware.rate_limiter import reset_rate_limit

reset_rate_limit(user_id=123, action='ai_requests')
print('✅ Rate limit reset')
"

# Посмотреть все ключи в Redis
redis-cli KEYS "rate_limit:*"

# Удалить все rate limit ключи
redis-cli KEYS "rate_limit:*" | xargs redis-cli DEL
```

### Cache управление

```bash
# Посмотреть статистику кэша
python -c "
from utils.cache import ai_chat_cache

stats = ai_chat_cache.get_stats()
print(f'Total keys: {stats[\"total_keys\"]}')
print(f'Total size: {stats[\"total_size_kb\"]} KB')
"

# Очистить кэш
python -c "
from utils.cache import ai_chat_cache

cleared = ai_chat_cache.clear_all()
print(f'✅ Cleared {cleared} cache entries')
"

# Посмотреть все кэш ключи
redis-cli KEYS "ai_chat:*"
```

---

## 🎯 Быстрые команды (Cheat Sheet)

```bash
# === РАЗРАБОТКА ===
# Запустить всё
docker-compose up -d && celery -A celery_app worker -l info --pool=solo & python main.py

# Тесты с покрытием
pytest --cov=. --cov-report=term-missing

# Проверить конфигурацию
python check_setup.py

# === БАЗА ДАННЫХ ===
# Подключиться
psql -h localhost -U ai_bot_user -d ai_bot_db

# Backup
pg_dump -h localhost -U ai_bot_user ai_bot_db > backup.sql

# Миграции
python migrate_db.py

# === ОТЛАДКА ===
# Логи Docker
docker-compose logs -f

# Проверить Redis
redis-cli ping

# Проверить PostgreSQL
psql -h localhost -U ai_bot_user -d ai_bot_db -c "SELECT 1;"

# === PRODUCTION ===
# Deploy на Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/ai-bot
gcloud run deploy ai-business-bot --image gcr.io/PROJECT_ID/ai-bot

# Логи Cloud Run
gcloud run logs read --service ai-business-bot

# === ОЧИСТКА ===
# Очистить кэш
redis-cli FLUSHALL

# Очистить Celery очередь
celery -A celery_app purge

# Удалить __pycache__
find . -type d -name __pycache__ -exec rm -rf {} +
```

---

## 🆘 Частые проблемы и решения

### Проблема: "Module not found"
```bash
# Переустановить зависимости
pip install --force-reinstall -r requirements.txt

# Проверить виртуальное окружение
which python
```

### Проблема: "Database connection failed"
```bash
# Проверить Docker
docker-compose ps

# Перезапустить PostgreSQL
docker-compose restart postgres

# Проверить переменные
echo $DB_HOST $DB_PORT
```

### Проблема: "Celery worker not starting"
```bash
# Windows: используйте --pool=solo
celery -A celery_app worker --loglevel=info --pool=solo

# Очистить очередь
celery -A celery_app purge
```

### Проблема: "Gemini API error"
```bash
# Проверить ключ
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('GEMINI_API_KEY')[:10])"

# Тест подключения
python -c "
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-pro-002')
print(model.generate_content('Test').text)
"
```

---

**Создано:** 2025-11-10
**Версия:** 2.0 (Gemini 1.5 Pro)
**Автор:** AI Business Assistant Team
