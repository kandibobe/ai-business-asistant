# 🚀 START HERE - Инструкция по запуску веб-приложения

## Быстрый старт (5 минут)

### Шаг 1: Установка зависимостей

```bash
# Python зависимости (Backend)
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib bcrypt python-multipart google-generativeai alembic python-dotenv

# Node.js зависимости (Frontend)
cd web-app
npm install
cd ..
```

### Шаг 2: Настройка окружения

Создайте файл `.env` в корне проекта:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ai_business_assistant
JWT_SECRET=your-super-secret-key-12345
GEMINI_API_KEY=your-gemini-api-key
```

**Получить Gemini API Key:** https://makersuite.google.com/app/apikey

### Шаг 3: Инициализация базы данных

```bash
# Создайте БД в PostgreSQL
psql -U postgres -c "CREATE DATABASE ai_business_assistant;"

# Создайте таблицы
python -c "from database.database import create_tables; create_tables()"
```

### Шаг 4: Запуск приложений

**Терминал 1 - Backend API:**
```bash
./start_api.sh
# Или: uvicorn api.main:app --reload --port 8000
```

**Терминал 2 - Frontend Web App:**
```bash
cd web-app
npm run dev
```

### Шаг 5: Откройте в браузере

- **Web App:** http://localhost:5173
- **API Docs:** http://localhost:8000/api/docs

---

## 📋 Что проверить

### 1. Регистрация и вход
- Перейдите на http://localhost:5173
- Зарегистрируйтесь: username `testuser`, password `Test123456`
- Вы должны автоматически попасть на Dashboard

### 2. Dashboard
- Увидите 4 карточки со статистикой (пока все 0)
- Quick Actions кнопки
- Premium баннер внизу

### 3. Загрузка документа
- **Documents** → Select File → выберите любой файл
- Наблюдайте progress bar (0-100%)
- Файл появится в списке с кнопками **Activate** и **Delete**

### 4. AI Chat
- **Chat** → введите вопрос "What is this document about?"
- Нажмите Enter
- AI ответит через 2-5 секунд
- Время ответа отображается рядом с сообщением

### 5. Analytics
- **Analytics** → посмотрите статистику
- Графики по типам документов
- Performance insights

### 6. Settings
- **Settings** → измените язык, AI role, response style
- Нажмите **Save Changes**
- Увидите notification "Settings saved successfully!"

---

## ✅ Что работает (100%)

### Backend API ✅
- ✅ JWT Authentication (register, login, refresh, /me)
- ✅ Documents API (upload, list, delete, activate)
- ✅ Chat API с Gemini AI
- ✅ Analytics API (stats, dashboard)
- ✅ Settings API
- ✅ File validation (max 50MB)
- ✅ Error handling
- ✅ OpenAPI docs

### Frontend Web App ✅
- ✅ Login/Register формы
- ✅ Dashboard с реальной статистикой
- ✅ Documents page (загрузка, удаление, активация)
- ✅ Chat с реальным AI
- ✅ Analytics с графиками
- ✅ Settings с сохранением
- ✅ Error Boundary
- ✅ Notifications
- ✅ Loading states
- ✅ Responsive design

---

## 📁 Структура проекта

```
ai-business-asistant/
├── api/                      # Backend FastAPI
│   ├── main.py              # Главный файл API
│   ├── dependencies.py      # Auth и DB
│   ├── routes/              # API endpoints
│   │   ├── auth.py          # Аутентификация
│   │   ├── documents.py     # Документы
│   │   ├── chat.py          # Чат с AI
│   │   ├── analytics.py     # Аналитика
│   │   └── settings.py      # Настройки
│   ├── models/              # Pydantic схемы
│   └── middleware/          # Middleware

├── web-app/                 # Frontend React
│   ├── src/
│   │   ├── api/services/    # API клиенты
│   │   ├── components/      # React компоненты
│   │   │   ├── ErrorBoundary.tsx
│   │   │   └── layout/MainLayout.tsx
│   │   ├── pages/           # Страницы
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── DocumentsPage.tsx
│   │   │   ├── ChatPage.tsx
│   │   │   ├── AnalyticsPage.tsx
│   │   │   └── SettingsPage.tsx
│   │   ├── store/           # Redux store
│   │   └── App.tsx          # Главный компонент

├── database/                # Database models
├── utils/                   # Utilities

├── .env                     # Environment variables
├── QUICKSTART.md           # Полное руководство
├── API_README.md           # API документация
├── WEB_APP_README.md       # Web App документация
└── START_HERE.md           # ЭТО ← Начните отсюда!
```

---

## 🎯 Основные endpoints

### Authentication
```bash
POST /api/auth/register     # Регистрация
POST /api/auth/login        # Вход
GET  /api/auth/me           # Текущий пользователь
POST /api/auth/refresh      # Обновить токен
```

### Documents
```bash
GET  /api/documents                # Список документов
POST /api/documents/upload         # Загрузить файл
GET  /api/documents/{id}           # Получить документ
DELETE /api/documents/{id}         # Удалить документ
PUT  /api/documents/{id}/activate  # Активировать документ
```

### Chat
```bash
POST /api/chat/message      # Отправить сообщение AI
GET  /api/chat/history      # История чата
DELETE /api/chat/history    # Очистить историю
WebSocket /api/chat/ws      # Real-time чат (скоро)
```

### Analytics
```bash
GET /api/analytics/stats                  # Статистика пользователя
GET /api/analytics/dashboard              # Dashboard данные
GET /api/analytics/documents/{id}/stats   # Статистика документа
```

### Settings
```bash
GET /api/settings           # Получить настройки
PUT /api/settings           # Обновить настройки
```

---

## 🔧 Troubleshooting

### Проблема: "ModuleNotFoundError"
**Решение:**
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib bcrypt python-multipart google-generativeai
```

### Проблема: "Database connection failed"
**Решение:**
1. Запустите PostgreSQL
2. Проверьте DATABASE_URL в `.env`
3. Создайте БД: `psql -U postgres -c "CREATE DATABASE ai_business_assistant;"`

### Проблема: "CORS error"
**Решение:** Уже настроено в api/main.py, просто перезапустите API

### Проблема: "Port already in use"
**Решение:**
```bash
# Для API (port 8000)
lsof -ti:8000 | xargs kill -9

# Для Web App (port 5173)
lsof -ti:5173 | xargs kill -9
```

---

## 📚 Полная документация

- **QUICKSTART.md** - Подробное руководство с примерами
- **API_README.md** - Полная документация API
- **WEB_APP_README.md** - Руководство по веб-приложению
- **WEB_APP_PROGRESS.md** - Детальный прогресс разработки

---

## 🎨 Демо-сценарий (5 минут)

### 1. Регистрация (30 сек)
```
Username: demo
Password: Demo123456
Email: demo@example.com
```

### 2. Загрузка документа (1 мин)
- Перейдите в Documents
- Загрузите любой PDF или Excel файл
- Дождитесь 100% progress
- Нажмите "Activate"

### 3. AI Chat (2 мин)
```
Вопрос 1: What is this document about?
Вопрос 2: Give me a summary of key points
Вопрос 3: What are the main topics?
```

### 4. Посмотрите статистику (1 мин)
- Dashboard → увидите обновленную статистику
- Analytics → графики и charts
- Settings → измените язык на Русский

### 5. Готово! (30 сек)
Вы протестировали все основные функции! 🎉

---

## 💡 Советы

### Для разработки:
1. **DevTools (F12)** - смотрите Console для ошибок
2. **Network tab** - проверяйте API запросы
3. **Redux DevTools** - отслеживайте state
4. **API Docs** - http://localhost:8000/api/docs для тестирования endpoints

### Для тестирования:
1. Попробуйте разные типы файлов (PDF, Excel, Word)
2. Задавайте разные вопросы AI
3. Проверьте все страницы
4. Попробуйте ошибки (неправильный пароль, большой файл >50MB)

### Для deployment:
1. Измените JWT_SECRET на случайную строку
2. Используйте production БД
3. Настройте HTTPS
4. Включите rate limiting

---

## 🔥 Быстрые команды

```bash
# Запуск всего (в разных терминалах)
./start_api.sh                    # Terminal 1: API
cd web-app && npm run dev         # Terminal 2: Web App

# Проверка здоровья
curl http://localhost:8000/health

# Просмотр логов
tail -f api/logs/app.log          # Если логирование настроено

# Пересоздание БД
python -c "from database.database import drop_tables, create_tables; drop_tables(); create_tables()"

# Build для production
cd web-app && npm run build
```

---

## 📞 Поддержка

- **GitHub Issues:** https://github.com/kandibobe/ai-business-asistant/issues
- **Documentation:** См. файлы в корне проекта
- **API Docs:** http://localhost:8000/api/docs (когда API запущен)

---

## 🎯 Следующие шаги

После успешного запуска:

1. ✅ **Протестируйте все функции** (следуйте демо-сценарию выше)
2. ✅ **Изучите код** (начните с api/main.py и web-app/src/App.tsx)
3. ✅ **Добавьте свои фичи** (см. TODO списки в коде)
4. ✅ **Деплой** (настройте для production)

---

**Готово! Теперь у вас работающее веб-приложение! 🚀**

Начните с запуска API и Web App, затем откройте браузер на http://localhost:5173

Удачи! 🎉
