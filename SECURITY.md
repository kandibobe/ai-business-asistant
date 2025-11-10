# 🔒 Руководство по безопасности

> Документация по функциям безопасности в AI Business Assistant

---

## 📋 Обзор

Проект реализует многоуровневую защиту:

1. **Валидация входных данных** - проверка файлов и текста
2. **Rate Limiting** - защита от спама и злоупотреблений
3. **Санитизация** - очистка потенциально опасного контента
4. **Безопасное хранение** - защита API ключей

---

## 🛡️ Защита файлов

### Валидация при загрузке

Каждый загружаемый файл проходит 3 уровня проверки:

```python
from utils.security import validate_file

# Автоматически проверяется:
# 1. Расширение файла (только разрешенные типы)
# 2. Размер файла (лимиты по типу)
# 3. MIME-type через magic bytes (защита от подделки расширения)

is_valid, error_msg = validate_file(
    file_path="/path/to/file.pdf",
    filename="document.pdf",
    file_type="pdf"
)
```

### Лимиты размеров файлов

```python
MAX_FILE_SIZES = {
    'pdf': 50 MB,
    'excel': 20 MB,
    'word': 20 MB,
    'audio': 25 MB,
}
```

### Разрешенные форматы

| Тип      | Расширения           | MIME Types                                   |
|----------|----------------------|----------------------------------------------|
| PDF      | `.pdf`               | `application/pdf`                            |
| Excel    | `.xlsx`, `.xls`      | Various Excel MIME types                     |
| Word     | `.docx`, `.doc`      | Various Word MIME types                      |
| Audio    | `.mp3`, `.wav`, etc. | `audio/mpeg`, `audio/wav`, `audio/ogg`, etc. |

### Защита от Path Traversal

Все имена файлов санитизируются:

```python
from utils.security import sanitize_filename

# Опасное имя
dangerous = "../../etc/passwd"

# Безопасное имя
safe = sanitize_filename(dangerous)  # -> "passwd"
```

---

## 🚦 Rate Limiting

### Лимиты по tier

```python
RATE_LIMITS = {
    'free': {
        'ai_requests': 5 запросов в минуту,
        'document_upload': 3 загрузки в 5 минут,
        'api_calls': 30 запросов в минуту,
    },
    'premium': {
        'ai_requests': 20 запросов в минуту,
        'document_upload': 10 загрузок в 5 минут,
        'api_calls': 100 запросов в минуту,
    },
}
```

### Использование в Telegram bot

```python
from middleware.rate_limiter import rate_limit

@rate_limit('ai_requests')
async def handle_message(update, context):
    # Автоматически проверяется лимит
    # Если превышен - пользователь получает сообщение
    # с информацией о лимите и времени ожидания
    pass
```

### Использование в FastAPI

```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/chat")
@limiter.limit("10/minute")
async def send_message():
    # Автоматически защищено rate limiting
    pass
```

### Проверка лимитов вручную

```python
from middleware.rate_limiter import check_rate_limit, get_rate_limit_info

# Проверка
try:
    check_rate_limit(user_id=123, action='ai_requests')
    # Лимит не превышен, можно продолжать
except RateLimitExceeded as e:
    print(f"Превышен лимит: {e.limit} req/{e.window}s")
    print(f"Попробуйте через: {e.retry_after} сек")

# Получение информации
info = get_rate_limit_info(user_id=123, action='ai_requests')
# {
#     'tier': 'free',
#     'limit': 5,
#     'current': 3,
#     'remaining': 2,
#     'reset_in': 45
# }
```

---

## 🧹 Санитизация входных данных

### Защита от SQL Injection

```python
from utils.security import sanitize_text_input, SecurityError

try:
    # Опасный ввод
    user_input = "'; DROP TABLE users; --"

    # Проверка
    clean_input = sanitize_text_input(user_input)
except SecurityError as e:
    # Обнаружен опасный паттерн
    print("Потенциальная SQL инъекция!")
```

### Защита от Command Injection

```python
try:
    dangerous = "test && rm -rf /"
    sanitize_text_input(dangerous)
except SecurityError:
    # Обнаружена попытка command injection
    pass
```

### Проверенные паттерны

- **SQL Injection:** `UNION SELECT`, `DROP TABLE`, `INSERT INTO`, `DELETE FROM`, `;`, `--`, `/* */`
- **Command Injection:** `&&`, `||`, `;`, `$(`, `` ` ``, `> /dev/`, `< /dev/`

---

## 🌐 Валидация URL

### Защита от SSRF

```python
from utils.security import validate_url

# Проверка URL перед скрапингом
is_valid, error_msg = validate_url("https://example.com")

if not is_valid:
    print(f"URL заблокирован: {error_msg}")
```

### Блокируются:

- ❌ `localhost` и `127.0.0.1`
- ❌ Локальные IP-адреса (`192.168.x.x`, `10.x.x.x`, `172.16-31.x.x`)
- ❌ Схемы `file://`, `ftp://`, `data:`
- ❌ URL длиннее 2000 символов

### Разрешаются:

- ✅ `http://` и `https://` схемы
- ✅ Публичные домены и IP-адреса

---

## 🔐 Безопасное хранение секретов

### .env файл

**НИКОГДА** не коммитьте `.env` в Git!

```bash
# В .gitignore должно быть:
.env
.env.local
.env.*.local
```

### Использование переменных окружения

```python
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Правильно
API_KEY = os.getenv('GEMINI_API_KEY')

# ❌ Неправильно
API_KEY = "sk-1234567890abcdef"  # Хардкод ключа
```

### Проверка наличия ключей

```python
REQUIRED_VARS = ['TELEGRAM_BOT_TOKEN', 'GEMINI_API_KEY', 'DB_PASS']

for var in REQUIRED_VARS:
    if not os.getenv(var):
        raise ValueError(f"⚠️ {var} не установлен в .env!")
```

---

## 🚨 Security Headers (для API)

### CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # НЕ "*" в production!
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Content Security Policy

```python
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response
```

---

## 📊 Мониторинг безопасности

### Логирование подозрительной активности

```python
import logging

logger = logging.getLogger("security")

# При обнаружении опасных паттернов
logger.warning(
    "Potential SQL injection attempt",
    extra={
        "user_id": user.id,
        "input": user_input[:100],  # Первые 100 символов
        "ip_address": request.client.host,
    }
)
```

### Metrics для Prometheus

```python
from prometheus_client import Counter

security_violations = Counter(
    'security_violations_total',
    'Total security violations detected',
    ['type', 'severity']
)

# При обнаружении
security_violations.labels(type='sql_injection', severity='high').inc()
```

---

## ✅ Checklist безопасности

### Перед deploy

- [ ] `.env` не в Git
- [ ] Все секреты в переменных окружения
- [ ] Rate limiting настроен
- [ ] Валидация файлов включена
- [ ] CORS настроен правильно (не "*")
- [ ] Security headers добавлены
- [ ] HTTPS включен
- [ ] Логирование безопасности работает
- [ ] Backup базы данных настроен
- [ ] Мониторинг подозрительной активности

### Регулярные проверки

- [ ] Обновление зависимостей (`pip list --outdated`)
- [ ] Проверка security advisories на GitHub
- [ ] Ревью логов безопасности
- [ ] Тестирование восстановления из backup
- [ ] Аудит прав доступа к БД

---

## 🐛 Баг-баунти

Если вы обнаружили уязвимость:

1. **НЕ создавайте публичный issue на GitHub**
2. Отправьте email: security@yourproject.com
3. Включите:
   - Описание уязвимости
   - Шаги для воспроизведения
   - Потенциальное влияние
   - Предложенное решение (опционально)

---

## 📚 Дополнительные ресурсы

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Telegram Bot Security](https://core.telegram.org/bots/webhooks#the-short-version)

---

**Последнее обновление:** 2025-11-09
**Версия:** 1.0
