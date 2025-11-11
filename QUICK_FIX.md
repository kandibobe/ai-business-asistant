# 🔧 Быстрое исправление ошибок

## Обнаруженные проблемы:

### ❌ Проблема 1: JWT_SECRET_KEY слишком короткий
```
1 validation error for Settings
jwt_secret_key
  Field required [type=missing, input_value={...}, input_type=dict]
```

**Решение:**
Откройте `.env` файл и убедитесь, что `JWT_SECRET_KEY` содержит минимум 32 символа:

```env
# В .env файле измените на:
JWT_SECRET_KEY=change-this-to-a-real-secret-key-min-32-characters-long-please
```

Или сгенерируйте свой ключ:
```bash
# На Windows (PowerShell):
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})

# На Linux/Mac:
openssl rand -hex 32
```

---

### ❌ Проблема 2: Multiple head revisions в Alembic
```
ERROR [alembic.util.messaging] Multiple head revisions are present
```

**Решение:** Используйте простой скрипт миграции вместо Alembic:

```bash
# Запустите скрипт миграции
python add_role_field_migration.py
```

Этот скрипт:
- ✅ Проверит существует ли поле `role`
- ✅ Добавит поле если его нет
- ✅ Создаст индекс для производительности
- ✅ Установит значение по умолчанию 'free' для существующих пользователей

---

### ❌ Проблема 3: ModuleNotFoundError: No module named 'migrate_language'

**Решение:** Уже исправлено! Этот импорт был удален из `main.py`.

---

## ✅ Пошаговое исправление:

### Шаг 1: Обновите .env файл

```bash
# Скопируйте пример если .env не существует
cp .env.example .env

# Откройте и проверьте JWT_SECRET_KEY (должен быть минимум 32 символа)
nano .env  # или любой редактор
```

Убедитесь что эти параметры заполнены:
```env
TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
GEMINI_API_KEY=ваш_ключ_gemini
JWT_SECRET_KEY=change-this-to-a-real-secret-key-min-32-characters-long-please
DB_USER=ai_bot_user
DB_PASS=your_strong_password_here
DB_NAME=ai_bot_db
```

### Шаг 2: Проверьте конфигурацию

```bash
python -m config.settings
```

Должно показать:
```
✅ Configuration loaded successfully!
```

### Шаг 3: Запустите миграцию для добавления поля role

```bash
python add_role_field_migration.py
```

Должно показать:
```
✅ Migration completed successfully!
```

### Шаг 4: Запустите приложение

```bash
# Запустите Celery worker (в отдельном терминале)
celery -A celery_app worker --loglevel=info --pool=solo

# Запустите бота
python main.py
```

---

## 🧪 Тесты компонентов

После исправления проверьте каждый компонент:

```bash
# 1. Конфигурация
python -m config.settings

# 2. LLM сервис
python -m services.llm_service

# 3. RBAC система
python -m services.rbac

# 4. Логирование
python -m utils.logger

# 5. Обработка ошибок
python -m utils.error_handlers
```

Все тесты должны завершиться с `✅ All tests completed!`

---

## 📝 Дополнительные советы

### Если проблемы с PostgreSQL:

```bash
# Проверьте что PostgreSQL запущен
docker-compose ps

# Если нет, запустите
docker-compose up -d

# Проверьте подключение
psql -h localhost -U ai_bot_user -d ai_bot_db
```

### Если проблемы с Redis:

```bash
# Проверьте Redis
redis-cli ping
# Должно вернуть: PONG

# Если нет, запустите через docker-compose
docker-compose up -d redis
```

---

## 🆘 Если ничего не помогло

1. **Полная переустановка зависимостей:**
```bash
# Удалите виртуальное окружение
rm -rf .venv

# Создайте заново
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# или
.venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt
```

2. **Сброс базы данных (УДАЛИТ ВСЕ ДАННЫЕ!):**
```bash
docker-compose down -v
docker-compose up -d
python add_role_field_migration.py
```

3. **Проверьте логи:**
```bash
# Логи бота
python main.py 2>&1 | tee bot.log

# Логи Celery
celery -A celery_app worker --loglevel=debug
```

---

## 📚 Полезные ссылки

- [ARCHITECTURE_IMPROVEMENTS.md](./ARCHITECTURE_IMPROVEMENTS.md) - Полное руководство по архитектуре
- [README.md](./README.md) - Основная документация
- [DEPLOYMENT.md](./DEPLOYMENT.md) - Production deployment
- [SECURITY.md](./SECURITY.md) - Безопасность

---

Если проблемы сохраняются, создайте issue на GitHub с полным описанием ошибки и логами.
