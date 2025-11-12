# 🚀 Quick Start Guide

Быстрый старт для запуска AI Business Assistant локально за 10 минут.

---

## 📋 Предварительные требования

Убедитесь, что у вас установлено:

- ✅ **Python 3.10+** - [Download](https://www.python.org/downloads/)
- ✅ **Docker & Docker Compose** - [Download](https://www.docker.com/get-started)
- ✅ **Git** - [Download](https://git-scm.com/downloads/)
- ✅ **Node.js 18+** (для веб-приложения) - [Download](https://nodejs.org/)

---

## ⚡ Быстрый запуск (3 шага)

### Шаг 1: Клонируйте репозиторий

```bash
git clone https://github.com/kandibobe/ai-business-asistant.git
cd ai-business-asistant
```

### Шаг 2: Настройте .env файл

```bash
# Создайте .env из примера
cp .env.example .env

# Отредактируйте .env и добавьте свои API ключи:
# - TELEGRAM_BOT_TOKEN (получите у @BotFather)
# - GEMINI_API_KEY (получите на https://makersuite.google.com/)
# - OPENAI_API_KEY (опционально, для транскрипции аудио)
```

**Минимальная конфигурация для тестирования:**

```env
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
GEMINI_API_KEY=ваш_gemini_api_ключ
DB_USER=ai_bot_user
DB_PASS=test_password_123
DB_NAME=ai_bot_db
JWT_SECRET_KEY=development-secret-key-min-32-characters-long
```

### Шаг 3: Запустите с Docker

```bash
# Запустите все сервисы (PostgreSQL, Redis, Bot, Worker)
docker-compose up -d

# Проверьте статус
docker-compose ps

# Просмотрите логи
docker-compose logs -f bot
```

🎉 **Готово!** Бот запущен и работает!

Протестируйте в Telegram: отправьте `/start` вашему боту.

---

## 🔧 Детальная установка (без Docker)

Если вы хотите запустить без Docker для разработки:

### 1. Установите зависимости PostgreSQL и Redis

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib redis-server
```

#### macOS:
```bash
brew install postgresql redis
brew services start postgresql
brew services start redis
```

#### Windows:
- PostgreSQL: https://www.postgresql.org/download/windows/
- Redis: https://github.com/microsoftarchive/redis/releases

### 2. Создайте базу данных

```bash
# Войдите в PostgreSQL
sudo -u postgres psql

# Создайте пользователя и базу
CREATE USER ai_bot_user WITH PASSWORD 'your_password';
CREATE DATABASE ai_bot_db OWNER ai_bot_user;
GRANT ALL PRIVILEGES ON DATABASE ai_bot_db TO ai_bot_user;
\q
```

### 3. Установите Python зависимости

```bash
# Создайте виртуальное окружение
python -m venv .venv

# Активируйте
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Установите зависимости
pip install -r requirements.txt
```

### 4. Примените миграции базы данных

```bash
# Примените миграции
alembic upgrade head
```

### 5. Запустите компоненты

**Терминал 1 - Celery Worker:**
```bash
celery -A celery_app worker --loglevel=info
```

**Терминал 2 - Telegram Bot:**
```bash
python main.py
```

**Терминал 3 (опционально) - REST API:**
```bash
python run_api.py
```

**Терминал 4 (опционально) - Web App:**
```bash
cd web-app
npm install
npm run dev
```

---

## 🌐 Запуск веб-приложения

### 1. Настройте .env для веб-приложения

```bash
cd web-app
cp .env.example .env
```

Отредактируйте `web-app/.env`:

```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_APP_NAME=AI Business Assistant
```

### 2. Установите и запустите

```bash
# Установите зависимости
npm install

# Запустите в dev режиме
npm run dev
```

Откройте браузер: http://localhost:5173

---

## 🧪 Проверка установки

### Проверьте, что все работает:

```bash
# 1. Проверьте PostgreSQL
psql -h localhost -U ai_bot_user -d ai_bot_db -c "SELECT version();"

# 2. Проверьте Redis
redis-cli ping
# Ожидается: PONG

# 3. Проверьте API (если запущено)
curl http://localhost:8000/health
# Ожидается: {"status": "healthy"}

# 4. Проверьте настройки Python
python -m config.settings
# Должно показать все настройки без ошибок
```

### Проверьте Docker сервисы:

```bash
# Проверьте статус
docker-compose ps

# Все сервисы должны быть "Up":
# - ai_bot_postgres_db
# - ai_bot_redis
# - ai_bot_app
# - ai_bot_worker

# Просмотрите логи
docker-compose logs bot
docker-compose logs worker
```

---

## 🎯 Первое использование

### 1. Telegram Bot

1. Найдите вашего бота в Telegram (используйте имя, которое дали @BotFather)
2. Отправьте `/start` - должно появиться приветствие
3. Загрузите тестовый документ (PDF, Excel, Word)
4. Дождитесь обработки
5. Задайте вопрос о документе

### 2. Web App

1. Откройте http://localhost:5173
2. Зарегистрируйтесь или войдите
3. Загрузите документ через интерфейс
4. Используйте чат для вопросов

---

## 📊 Мониторинг

### Prometheus & Grafana (опционально)

```bash
# Запустите мониторинг стек
docker-compose -f docker-compose.monitoring.yml up -d

# Откройте Grafana
open http://localhost:3000
# Логин: admin / admin

# Импортируйте dashboard
# В Grafana: Import → Upload → monitoring/grafana_dashboard.json
```

---

## 🐛 Troubleshooting

### Проблема: "Port 5432 already in use"

```bash
# Остановите локальный PostgreSQL
sudo systemctl stop postgresql  # Linux
brew services stop postgresql   # macOS

# Или измените порт в docker-compose.yml
```

### Проблема: "Permission denied" для Docker

```bash
# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER

# Перелогиньтесь или выполните
newgrp docker
```

### Проблема: "Module not found"

```bash
# Переустановите зависимости
pip install --upgrade -r requirements.txt

# Проверьте виртуальное окружение активировано
which python  # Должен показать путь к .venv
```

### Проблема: "Database connection failed"

```bash
# Проверьте, что PostgreSQL запущен
docker-compose ps db
# или
sudo systemctl status postgresql

# Проверьте credentials в .env
# DB_HOST, DB_PORT, DB_USER, DB_PASS, DB_NAME
```

### Проблема: "Redis connection failed"

```bash
# Проверьте, что Redis запущен
docker-compose ps redis
# или
redis-cli ping

# Проверьте REDIS_URL в .env
```

### Проблема: Celery worker не запускается

```bash
# Убедитесь, что Redis работает
redis-cli ping

# Запустите worker с более подробными логами
celery -A celery_app worker --loglevel=debug

# Проверьте очередь задач
celery -A celery_app inspect active
```

---

## 🔄 Обновление

```bash
# Остановите сервисы
docker-compose down

# Получите последние изменения
git pull origin main

# Примените новые миграции
docker-compose run bot alembic upgrade head

# Перезапустите
docker-compose up -d

# Обновите веб-приложение
cd web-app
npm install
npm run build
```

---

## 🧹 Очистка

### Остановить и удалить контейнеры:

```bash
# Остановить все сервисы
docker-compose down

# Удалить с volumes (ВНИМАНИЕ: удалит данные!)
docker-compose down -v

# Удалить images
docker-compose down --rmi all
```

### Очистить данные:

```bash
# Удалить загруженные файлы
rm -rf downloads/*

# Удалить логи
rm -rf logs/*

# Очистить кэш Redis
redis-cli FLUSHALL
```

---

## 📚 Следующие шаги

После успешного запуска:

1. **Изучите документацию:**
   - [README.md](README.md) - Обзор проекта
   - [ARCHITECTURE.md](ARCHITECTURE.md) - Архитектура
   - [DEPLOYMENT.md](DEPLOYMENT.md) - Production deployment
   - [CONTRIBUTING.md](CONTRIBUTING.md) - Как контрибьютить

2. **Настройте monitoring:**
   - Импортируйте Grafana dashboard
   - Настройте Sentry для error tracking
   - Настройте alerts

3. **Запустите тесты:**
   ```bash
   pytest
   pytest --cov=. --cov-report=html
   ```

4. **Настройте pre-commit hooks:**
   ```bash
   pip install pre-commit
   pre-commit install
   pre-commit run --all-files
   ```

5. **Подготовьте к production:**
   - Замените test credentials на production
   - Настройте HTTPS
   - Настройте backup базы данных
   - Настройте CI/CD

---

## 🆘 Получить помощь

- **Issues:** [GitHub Issues](https://github.com/kandibobe/ai-business-asistant/issues)
- **Discussions:** [GitHub Discussions](https://github.com/kandibobe/ai-business-asistant/discussions)
- **Documentation:** Смотрите другие .md файлы в корне проекта

---

## ✅ Checklist быстрого старта

- [ ] Python 3.10+ установлен
- [ ] Docker установлен и запущен
- [ ] Репозиторий клонирован
- [ ] .env файл создан и заполнен
- [ ] Получены API ключи (Telegram Bot Token, Gemini API Key)
- [ ] `docker-compose up -d` выполнен успешно
- [ ] Все 4 контейнера запущены (db, redis, bot, worker)
- [ ] Бот отвечает на `/start` в Telegram
- [ ] (Опционально) Веб-приложение запущено на localhost:5173
- [ ] (Опционально) API работает на localhost:8000

---

**Время установки:** ~10 минут
**Сложность:** ⭐⭐☆☆☆ (Легко)

**Удачи! 🚀**
