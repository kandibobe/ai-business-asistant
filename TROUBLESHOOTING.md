# 🔧 Руководство по устранению неполадок

> Полное руководство по решению распространенных проблем

---

## 🚨 Частые проблемы и решения

### 1. ❌ JWT_SECRET_KEY validation error

**Ошибка:**
```
1 validation error for Settings
jwt_secret_key
  Field required [type=missing]
```

**Причина:** JWT ключ в .env файле отсутствует или слишком короткий (< 32 символов)

**Решение А: Автоматическое (рекомендуется)**
```bash
python fix_env_jwt.py
```

**Решение Б: Ручное**
1. Откройте `.env` файл
2. Найдите или добавьте строку:
```env
JWT_SECRET_KEY=your-very-long-secret-key-at-least-32-characters-long
```
3. Сгенерируйте безопасный ключ:
```powershell
# Windows PowerShell
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 48 | % {[char]$_})

# Linux/Mac
openssl rand -hex 32
```

**Проверка:**
```bash
python -m config.settings
```

---

### 2. ❌ RBAC module error: NameError

**Ошибка:**
```
NameError: name 'ROLE_DEFINITIONS' is not defined
```

**Причина:** Циклическая зависимость в определении ролей

**Решение:** ✅ Уже исправлено в последнем коммите

**Проверка:**
```bash
python -c "from services.rbac import RBACService; print('✅ RBAC OK')"
```

---

### 3. ❌ Database migration issues

**Ошибка:**
```
Multiple head revisions are present for given argument 'head'
```

**Решение:** Используйте простой скрипт миграции вместо Alembic
```bash
python add_role_field_migration.py
```

**Если нужно полностью пересоздать БД (УДАЛИТ ВСЕ ДАННЫЕ!):**
```bash
docker-compose down -v
docker-compose up -d
python add_role_field_migration.py
```

---

### 4. ❌ Тесты падают

**Проблема:** 6 failed tests при запуске pytest

**Решение:**

**А. Тест `test_document_defaults`:**
```bash
# Проверьте что processed_at определен в модели
grep "processed_at" database/models.py
```

**Б. Тесты `test_handle_*_document`:**
```bash
# Убедитесь что downloads директория существует
mkdir -p downloads

# Запустите только unit тесты
pytest tests/unit/ -v
```

**В. Windows file locking (Excel tests):**
- Закройте Excel если открыт
- Перезапустите pytest
- Используйте `pytest -n auto` для параллельного запуска

---

### 5. ❌ ModuleNotFoundError

**Ошибка:**
```
ModuleNotFoundError: No module named 'tenacity'
```

**Причина:** Не все зависимости установлены

**Решение:**
```bash
# Переустановите зависимости
pip install -r requirements.txt

# Или конкретный пакет
pip install tenacity==8.2.3
```

**Если используете Poetry:**
```bash
poetry install
poetry shell
```

---

### 6. ❌ LLM Service cannot initialize

**Ошибка:**
```
LLMError: Failed to initialize Gemini: argument of type 'NoneType' is not iterable
```

**Причина:** GEMINI_API_KEY не установлен или None

**Решение:**
1. Получите API ключ: https://makersuite.google.com/app/apikey
2. Добавьте в `.env`:
```env
GEMINI_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ123456
```

**Проверка:**
```bash
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('GEMINI_API_KEY:', os.getenv('GEMINI_API_KEY')[:20] + '...')"
```

---

### 7. ❌ Celery worker не запускается

**Windows:**
```bash
# Обязательно используйте --pool=solo на Windows!
celery -A celery_app worker --loglevel=info --pool=solo
```

**Linux/Mac:**
```bash
celery -A celery_app worker --loglevel=info
```

**Проверка Redis:**
```bash
redis-cli ping
# Должно вернуть: PONG
```

---

### 8. ❌ PostgreSQL connection refused

**Ошибка:**
```
could not connect to server: Connection refused
```

**Решение:**
```bash
# Проверьте что PostgreSQL запущен
docker-compose ps

# Если нет, запустите
docker-compose up -d postgres

# Проверьте подключение
psql -h localhost -U ai_bot_user -d ai_bot_db
```

**Проверьте .env:**
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=ai_bot_user
DB_PASS=ваш_пароль
DB_NAME=ai_bot_db
```

---

### 9. ⚠️ Deprecation warnings

**Warning:**
```
DeprecationWarning: datetime.datetime.utcnow() is deprecated
```

**Причина:** Устаревший API в Python 3.12+

**Решение:** Уже исправлено в следующей версии (используем `datetime.now(datetime.UTC)`)

**Временное решение:** Игнорируйте warning или установите Python 3.11

---

### 10. ❌ python-magic not available

**Warning:**
```
WARNING: python-magic not available. MIME type validation will be skipped.
```

**Windows:**
```bash
pip install python-magic-bin
```

**Linux:**
```bash
sudo apt-get install libmagic1
pip install python-magic
```

**Mac:**
```bash
brew install libmagic
pip install python-magic
```

---

## 🧪 Диагностические команды

### Проверка всех компонентов:

```bash
# 1. Конфигурация
python -m config.settings

# 2. Импорты модулей
python -c "from services.rbac import RBACService; print('✅ RBAC')"
python -c "from utils.logger import setup_logging; print('✅ Logger')"
python -c "from utils.error_handlers import AppError; print('✅ Errors')"
python -c "from database.models import User, Document; print('✅ Models')"

# 3. База данных
python -c "from database.database import engine; print('DB URL:', engine.url)"

# 4. Redis
redis-cli ping

# 5. Celery tasks
celery -A celery_app inspect registered
```

---

## 🔬 Запуск тестов

### Все тесты:
```bash
pytest
```

### Только unit тесты (быстро):
```bash
pytest tests/unit/ -v
```

### Только integration тесты:
```bash
pytest tests/integration/ -v
```

### Конкретный тест:
```bash
pytest tests/unit/test_models.py::TestDocumentModel::test_document_defaults -v
```

### С покрытием кода:
```bash
pytest --cov=. --cov-report=html
```

### Параллельно (быстрее):
```bash
pytest -n auto
```

### Игнорировать warnings:
```bash
pytest -W ignore::DeprecationWarning
```

---

## 🧹 Очистка и сброс

### Очистка кэша Python:
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Очистка pytest кэша:
```bash
rm -rf .pytest_cache htmlcov .coverage
```

### Пересоздание виртуального окружения:
```bash
# Удалить
rm -rf .venv

# Создать заново
python -m venv .venv

# Активировать
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

### Полный сброс БД и Redis:
```bash
docker-compose down -v
docker-compose up -d
python add_role_field_migration.py
```

---

## 📊 Проверка здоровья системы

### Скрипт быстрой проверки:

Создайте `health_check.py`:
```python
#!/usr/bin/env python3
import sys

checks = []

# 1. Imports
try:
    from config import get_settings
    checks.append(("Config", True, ""))
except Exception as e:
    checks.append(("Config", False, str(e)))

# 2. Database
try:
    from database.database import engine
    conn = engine.connect()
    conn.close()
    checks.append(("Database", True, ""))
except Exception as e:
    checks.append(("Database", False, str(e)))

# 3. Redis
try:
    import redis
    r = redis.from_url("redis://localhost:6379/0")
    r.ping()
    checks.append(("Redis", True, ""))
except Exception as e:
    checks.append(("Redis", False, str(e)))

# 4. Models
try:
    from database.models import User, Document
    checks.append(("Models", True, ""))
except Exception as e:
    checks.append(("Models", False, str(e)))

# Print results
print("\n" + "=" * 60)
print("🏥 System Health Check")
print("=" * 60)

all_ok = True
for name, ok, error in checks:
    status = "✅" if ok else "❌"
    print(f"{status} {name:15} ", end="")
    if not ok:
        print(f"Error: {error[:40]}")
        all_ok = False
    else:
        print("OK")

print("=" * 60)
if all_ok:
    print("✅ All systems operational!")
    sys.exit(0)
else:
    print("❌ Some systems failed. Check errors above.")
    sys.exit(1)
```

Запуск:
```bash
python health_check.py
```

---

## 🆘 Последнее средство

Если ничего не помогает:

1. **Сохраните важные данные:**
   ```bash
   # Экспорт БД
   pg_dump -h localhost -U ai_bot_user ai_bot_db > backup.sql
   ```

2. **Полная переустановка:**
   ```bash
   # Удалить все
   rm -rf .venv postgres_data redis_data

   # Остановить Docker
   docker-compose down -v

   # Клонировать заново
   git pull origin main

   # Установить с нуля
   python -m venv .venv
   source .venv/bin/activate  # или .venv\Scripts\activate на Windows
   pip install -r requirements.txt

   # Настроить .env
   cp .env.example .env
   nano .env  # заполнить все ключи

   # Запустить
   docker-compose up -d
   python add_role_field_migration.py
   python main.py
   ```

---

## 📞 Получение помощи

1. **Проверьте документацию:**
   - [README.md](./README.md)
   - [ARCHITECTURE_IMPROVEMENTS.md](./ARCHITECTURE_IMPROVEMENTS.md)
   - [QUICK_FIX.md](./QUICK_FIX.md)
   - [CRITICAL_FIXES.md](./CRITICAL_FIXES.md)

2. **Запустите диагностику:**
   ```bash
   python health_check.py
   python -m config.settings
   ```

3. **Соберите информацию:**
   ```bash
   python --version
   pip list
   docker-compose ps
   ```

4. **Создайте issue на GitHub:**
   - Опишите проблему
   - Приложите вывод диагностики
   - Укажите ОС и версию Python

---

**Версия:** 2.0.1
**Последнее обновление:** 2025-11-11
