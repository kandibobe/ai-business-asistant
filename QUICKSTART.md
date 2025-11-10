# 🚀 Quick Start Guide - AI Business Assistant

## Полное руководство по запуску и тестированию веб-приложения

---

## 📋 Содержание

1. [Требования](#требования)
2. [Установка](#установка)
3. [Настройка](#настройка)
4. [Запуск Backend API](#запуск-backend-api)
5. [Запуск Frontend Web App](#запуск-frontend-web-app)
6. [Тестирование](#тестирование)
7. [Troubleshooting](#troubleshooting)

---

## ✅ Требования

### Необходимые инструменты:
- **Python 3.10+** (для backend)
- **Node.js 18+** и **npm** (для frontend)
- **PostgreSQL 14+** (база данных)
- **Git** (для клонирования репозитория)

### Опционально:
- **Redis** (для кэширования, пока не реализовано)
- **Docker** (для контейнеризации, пока не реализовано)

---

## 📦 Установка

### 1. Клонируйте репозиторий (если еще не клонировали)

```bash
git clone https://github.com/kandibobe/ai-business-asistant.git
cd ai-business-asistant
```

### 2. Установите Python зависимости (Backend)

```bash
# Создайте виртуальное окружение (рекомендуется)
python3 -m venv venv

# Активируйте виртуальное окружение
# На Linux/Mac:
source venv/bin/activate
# На Windows:
# venv\Scripts\activate

# Установите зависимости
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib bcrypt python-multipart google-generativeai alembic python-dotenv
```

### 3. Установите Node.js зависимости (Frontend)

```bash
cd web-app
npm install
cd ..
```

---

## ⚙️ Настройка

### 1. Создайте файл `.env` в корне проекта

```bash
# В корне проекта (не в web-app!)
touch .env
```

Добавьте следующие переменные:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ai_business_assistant

# JWT Secret (измените на случайную строку!)
JWT_SECRET=your-super-secret-key-change-me-in-production-12345

# Gemini API Key (получите на https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your-gemini-api-key-here

# Optional: Redis
REDIS_URL=redis://localhost:6379
```

### 2. Настройте базу данных PostgreSQL

```bash
# Войдите в PostgreSQL
psql -U postgres

# Создайте базу данных
CREATE DATABASE ai_business_assistant;

# Создайте пользователя (если нужно)
CREATE USER your_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE ai_business_assistant TO your_user;

# Выйдите
\q
```

### 3. Инициализируйте базу данных

```bash
# Создайте таблицы
python -c "from database.database import create_tables; create_tables()"
```

### 4. Настройте Frontend (опционально)

```bash
cd web-app

# Создайте .env.local
cat > .env.local << EOF
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
EOF

cd ..
```

---

## 🔥 Запуск Backend API

### Вариант 1: Использовать скрипт (рекомендуется)

```bash
# Сделайте скрипт исполняемым
chmod +x start_api.sh

# Запустите API
./start_api.sh
```

### Вариант 2: Запуск вручную

```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Запустите uvicorn
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**API запущен!** 🎉

- **API URL:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

---

## 🌐 Запуск Frontend Web App

### В отдельном терминале:

```bash
cd web-app

# Запустите dev server
npm run dev
```

**Web App запущен!** 🎉

- **Web App URL:** http://localhost:5173

---

## 🧪 Тестирование

### Шаг 1: Откройте браузер

Откройте браузер и перейдите на **http://localhost:5173**

### Шаг 2: Регистрация

1. Нажмите на вкладку **"Sign Up"**
2. Заполните форму:
   - **Username:** testuser
   - **Password:** Test123456
   - **Email:** test@example.com (опционально)
   - **First Name:** Test
   - **Last Name:** User
3. Нажмите **"Sign Up"**

✅ Вы должны автоматически войти в систему и попасть на Dashboard

### Шаг 3: Проверьте Dashboard

На Dashboard вы увидите:
- **4 карточки** со статистикой (пока все 0)
- **Quick Actions** кнопки
- **Recent Documents** (пока пусто)
- **Premium Upgrade** баннер (если не premium)

### Шаг 4: Загрузите документ

1. Перейдите в **Documents** (боковое меню)
2. Нажмите **"Select File"**
3. Выберите любой документ (PDF, Excel, Word, txt)
4. Нажмите **"Upload"**
5. Наблюдайте progress bar (0-100%)

✅ Документ загружен! Вы увидите его в списке

**Функции документов:**
- **Activate** - активировать документ для чата
- **Delete** - удалить документ (с подтверждением)
- **Active badge** - показывает активный документ

### Шаг 5: Протестируйте AI Chat

1. Перейдите в **Chat** (боковое меню)
2. Активируйте документ если нужно (в Documents)
3. Введите вопрос: "What is this document about?"
4. Нажмите Enter или кнопку отправки

✅ AI ответит через 2-5 секунд

**Возможности чата:**
- Показывает время ответа (response time)
- Сохраняет историю
- Clear history кнопка
- Shift+Enter для новой строки

### Шаг 6: Проверьте Analytics

1. Перейдите в **Analytics**
2. Вы увидите:
   - Total Documents
   - Questions Asked
   - Average Response Time
   - Documents by Type (графики)
   - Performance Insights

### Шаг 7: Настройки

1. Перейдите в **Settings**
2. Измените:
   - **Language:** English / Русский / Deutsch
   - **AI Role:** Assistant / Analyst / Consultant
   - **Response Style:** Brief / Standard / Detailed
   - **AI Mode:** Fast / Standard / Advanced
3. Нажмите **"Save Changes"**

✅ Настройки сохранены!

### Шаг 8: Проверьте Error Boundary

Чтобы проверить Error Boundary (для разработчиков):

1. Откройте DevTools (F12)
2. В Console введите: `throw new Error("Test error")`
3. Вы увидите красивую страницу ошибки с кнопками:
   - **Try Again**
   - **Reload Page**

---

## 🎨 Основные функции

### ✅ Реализовано

#### Backend API
- ✅ JWT Authentication (register, login, refresh, /me)
- ✅ Document upload (max 50MB, multiple formats)
- ✅ AI Chat with Gemini API
- ✅ Analytics endpoints
- ✅ Settings management
- ✅ File validation
- ✅ Error handling
- ✅ OpenAPI docs

#### Frontend Web App
- ✅ Login/Register forms
- ✅ Dashboard with stats
- ✅ Documents page (upload, delete, activate)
- ✅ Chat page with real AI
- ✅ Analytics page with charts
- ✅ Settings page
- ✅ Error Boundary
- ✅ Notifications (Snackbar)
- ✅ Loading states
- ✅ Responsive design

### 🔄 Не реализовано (еще)
- ⏳ WebSocket real-time chat
- ⏳ Document preview
- ⏳ Export functionality
- ⏳ Search & filters
- ⏳ Premium payment integration
- ⏳ Unit tests
- ⏳ E2E tests

---

## 📱 Доступные страницы

### 1. **Dashboard** (`/dashboard`)
- Статистика пользователя
- Quick actions
- Recent documents
- Premium upgrade banner

### 2. **Documents** (`/documents`)
- Загрузка файлов
- Список документов
- Удаление документов
- Активация документов

### 3. **Chat** (`/chat`)
- AI чат с Gemini
- История сообщений
- Response time tracking
- Clear history

### 4. **Analytics** (`/analytics`)
- Total statistics
- Documents by type
- Performance insights
- Speed ratings

### 5. **Settings** (`/settings`)
- Profile info
- Language selection
- AI configuration
- Notifications toggle

### 6. **Premium** (`/premium`)
- Premium plans
- Feature comparison
- Upgrade options

---

## 🐛 Troubleshooting

### Backend не запускается

**Проблема:** `ModuleNotFoundError: No module named 'fastapi'`

**Решение:**
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib bcrypt python-multipart google-generativeai
```

---

**Проблема:** `Connection to database failed`

**Решение:**
1. Проверьте, что PostgreSQL запущен
2. Проверьте DATABASE_URL в `.env`
3. Создайте базу данных: `CREATE DATABASE ai_business_assistant;`

---

**Проблема:** `GEMINI_API_KEY not found`

**Решение:**
1. Получите API key на https://makersuite.google.com/app/apikey
2. Добавьте в `.env`: `GEMINI_API_KEY=your-key-here`

---

### Frontend не запускается

**Проблема:** `Cannot find module '@/store'`

**Решение:**
```bash
cd web-app
npm install
npm run dev
```

---

**Проблема:** `CORS error`

**Решение:**
Убедитесь что API разрешает `http://localhost:5173` в CORS origins (уже настроено в `api/main.py`)

---

**Проблема:** `401 Unauthorized`

**Решение:**
1. Проверьте что вы залогинены
2. Очистите localStorage: DevTools → Application → Local Storage → Clear
3. Перелогиньтесь

---

### Другие проблемы

**API не отвечает:**
```bash
# Проверьте запущен ли API
curl http://localhost:8000/health

# Ожидаемый ответ:
# {"status":"healthy","service":"AI Business Assistant API","version":"1.0.0"}
```

**Web App не загружается:**
```bash
# Проверьте порт 5173
lsof -ti:5173

# Если занят, убейте процесс:
lsof -ti:5173 | xargs kill -9
```

**Database проблемы:**
```bash
# Пересоздайте таблицы
python -c "from database.database import drop_tables, create_tables; drop_tables(); create_tables()"
```

---

## 🔧 Полезные команды

### Backend

```bash
# Запустить API
./start_api.sh

# Проверить здоровье API
curl http://localhost:8000/health

# Просмотреть логи API
uvicorn api.main:app --reload --log-level debug

# Создать миграцию Alembic (когда будет настроено)
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Frontend

```bash
cd web-app

# Запустить dev server
npm run dev

# Собрать для production
npm run build

# Просмотреть production build
npm run preview

# Проверить типы TypeScript
npm run type-check

# Форматировать код (если настроено)
npm run format
```

### Git

```bash
# Посмотреть статус
git status

# Посмотреть изменения
git diff

# Коммит
git add .
git commit -m "Your message"

# Пуш
git push
```

---

## 📞 Поддержка

Если у вас возникли проблемы:

1. **Проверьте логи:**
   - Backend: в терминале где запущен API
   - Frontend: Browser DevTools → Console

2. **Проверьте документацию:**
   - `API_README.md` - полная документация API
   - `WEB_APP_README.md` - руководство по веб-приложению
   - `WEB_APP_PROGRESS.md` - детальный прогресс

3. **Создайте Issue на GitHub:**
   https://github.com/kandibobe/ai-business-asistant/issues

---

## 🎯 Что дальше?

После успешного запуска и тестирования, вы можете:

1. **Добавить больше документов**
   - Попробуйте разные типы файлов (PDF, Excel, Word)
   - Тестируйте большие файлы (до 50MB)

2. **Задать больше вопросов AI**
   - Экспериментируйте с разными типами вопросов
   - Проверьте работу с активным документом

3. **Посмотреть аналитику**
   - Следите как растет статистика
   - Проверяйте response time

4. **Настроить под себя**
   - Измените AI role и style
   - Попробуйте разные языки

5. **Продолжить разработку**
   - Добавьте WebSocket
   - Реализуйте preview документов
   - Добавьте тесты

---

## 📚 Дополнительные ресурсы

- **API Documentation:** http://localhost:8000/api/docs (когда API запущен)
- **ReDoc:** http://localhost:8000/api/redoc
- **GitHub Repo:** https://github.com/kandibobe/ai-business-asistant

---

**Готово! Теперь у вас запущено и работает веб-приложение AI Business Assistant! 🎉**

Удачи в разработке! 🚀
