# 🤖 AI Business Assistant

**Интеллектуальный бизнес-ассистент** с Telegram ботом и веб-приложением на базе Google Gemini AI.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://www.typescriptlang.org/)

---

## ✨ Возможности

### 🌐 Веб-приложение
- 🎨 Красивая landing page
- 📊 Dashboard с аналитикой
- 📄 Управление документами (PDF, Excel, Word)
- 💬 AI Chat с контекстом документов
- 📈 Детальная аналитика использования
- ⚙️ Настройки пользователя

### 🤖 Telegram Bot
- 📤 Загрузка документов (PDF, Excel, Word, Audio)
- 💬 Вопросы к документам через AI
- 🎙️ Голосовые сообщения (транскрибация)
- 📊 Статистика и отчеты
- 🔔 Уведомления

### 🔌 Backend API
- 🔐 JWT авторизация
- 📚 RESTful API
- 🚀 Кэширование в Redis
- 🛡️ Rate limiting
- 📝 Swagger/ReDoc документация

---

## 🚀 Быстрый старт

### 1. Клонировать проект
```bash
git clone https://github.com/kandibobe/ai-business-asistant.git
cd ai-business-asistant
```

### 2. Создать .env файл
```bash
# Linux/Mac:
cp .env.example .env

# Windows:
copy .env.example .env
```

**Отредактируйте .env и добавьте:**
- `TELEGRAM_BOT_TOKEN` - от [@BotFather](https://t.me/BotFather)
- `GEMINI_API_KEY` - от [Google AI Studio](https://makersuite.google.com/)
- `JWT_SECRET_KEY` - сгенерируйте: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

### 3. Запустить Docker сервисы
```bash
docker-compose up -d
```

### 4. Установить зависимости
```bash
# Python
pip install -r requirements.txt

# Node.js
cd web-app
npm install
cd ..
```

### 5. Применить миграции БД
```bash
python upgrade_db.py
```

### 6. Запустить приложение

#### Вариант A: Автоматический запуск (рекомендуется)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

#### Вариант B: Ручной запуск

**Терминал 1 - Backend API:**
```bash
cd api
python main.py
```

**Терминал 2 - Web App:**
```bash
cd web-app
npm run dev
```

**Терминал 3 - Telegram Bot:**
```bash
python main.py
```

---

## 🌐 Доступ к приложению

После запуска откройте:

| Сервис | URL | Описание |
|--------|-----|----------|
| **Web App** | http://localhost:3000 | Веб-интерфейс |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Telegram Bot** | Ваш бот | Напишите `/start` |

---

## 📖 Подробная документация

- [**QUICKSTART.md**](./QUICKSTART.md) - Полное руководство по установке и запуску
- [**TOP_10_IMPROVEMENTS.md**](./TOP_10_IMPROVEMENTS.md) - Все улучшения проекта
- [**DEPLOYMENT.md**](./DEPLOYMENT.md) - Production deployment
- [**SESSION_SUMMARY.md**](./SESSION_SUMMARY.md) - Отчет о проделанной работе

---

## 🛠️ Технологии

### Backend:
- Python 3.9+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Celery
- Google Gemini AI

### Frontend:
- React 18
- TypeScript 5
- Material-UI 5
- Redux Toolkit
- Vite
- Axios

### Infrastructure:
- Docker & Docker Compose
- Nginx (production)
- Alembic (migrations)

---

## 📁 Структура проекта

```
ai-business-asistant/
├── api/                 # Backend API (FastAPI)
├── web-app/            # Frontend (React + TypeScript)
├── bot/                # Telegram Bot
├── database/           # Database models & CRUD
├── utils/              # Utilities & helpers
├── migrations/         # Database migrations
├── docker-compose.yml  # Docker configuration
├── start.bat           # Windows launcher
├── start.sh            # Linux/Mac launcher
└── README_RU.md        # This file
```

---

## 🐛 Troubleshooting

### Проблема: Port already in use

**Решение:**
```bash
# Linux/Mac:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Проблема: Database connection failed

**Решение:**
```bash
# Перезапустить Docker
docker-compose down
docker-compose up -d

# Применить миграции
python upgrade_db.py
```

### Проблема: Module not found

**Решение:**
```bash
# Переустановить зависимости
pip install -r requirements.txt --force-reinstall
```

### Проблема: Web app не открывается

**Решение:**
```bash
# Проверить что Backend API запущен
curl http://localhost:8000/api/health

# Переустановить Node зависимости
cd web-app
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 Мониторинг

### Проверка сервисов:
```bash
# Backend API
curl http://localhost:8000/api/health

# PostgreSQL
docker-compose exec postgres pg_isready

# Redis
docker-compose exec redis redis-cli ping
```

### Логи:
```bash
# Docker логи
docker-compose logs -f

# Backend логи
tail -f backend.log

# Web логи
tail -f web.log
```

---

## 🔒 Безопасность

✅ Никогда не коммитьте .env файл
✅ Используйте сильные пароли
✅ В production используйте HTTPS
✅ Регулярно обновляйте зависимости
✅ Настройте CORS правильно

---

## 📝 Лицензия

MIT License

---

## 🤝 Contributing

Мы приветствуем вклад в проект! 

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Создайте Pull Request

---

## 📞 Поддержка

Если у вас возникли проблемы:

1. Проверьте [QUICKSTART.md](./QUICKSTART.md)
2. Посмотрите [Troubleshooting](#troubleshooting)
3. Создайте [Issue на GitHub](https://github.com/kandibobe/ai-business-asistant/issues)

---

## ⭐ Star History

Если проект вам понравился, поставьте звезду! ⭐

---

**Создано с ❤️ для автоматизации бизнес-процессов**
