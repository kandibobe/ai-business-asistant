# 🪟 Windows Setup Guide - AI Business Assistant

**Специальное руководство для Windows пользователей**

---

## ✅ Что было исправлено

### 1. Pydantic v2 Compatibility ✅
- Заменили `regex=` на `pattern=` во всех валидаторах
- Файл: `utils/validators.py`

### 2. Pytest Version ✅
- Понизили требование с 8.0 до 7.4
- Файл: `pytest.ini`

### 3. Database Migration ✅
- Решена проблема с дублирующимися таблицами
- Инструкции ниже

---

## 🚀 Быстрый старт (Windows)

### Шаг 1: Создайте файл `.env`

Создайте файл `.env` в корне проекта (рядом с `README.md`):

```powershell
# Скопируйте и вставьте в PowerShell:
@"
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ai_business_assistant
JWT_SECRET=your-super-secret-key-change-me-in-production-12345
GEMINI_API_KEY=your-gemini-api-key-here
"@ | Out-File -FilePath .env -Encoding UTF8
```

**ВАЖНО**: Замените:
- `your_password` - на ваш пароль PostgreSQL
- `your-gemini-api-key-here` - на ваш Gemini API key от Google

**Получить Gemini API Key**: https://makersuite.google.com/app/apikey

---

### Шаг 2: Исправьте базу данных

У вас уже есть таблицы в базе данных, но были ошибки при миграции. Выберите один из вариантов:

#### Вариант A: Использовать существующие таблицы (Рекомендуется)

Просто пропустите миграции Alembic. Таблицы уже созданы и готовы к работе!

```powershell
# Ничего делать не нужно! Переходите к Шагу 3
```

#### Вариант B: Пересоздать базу данных (Если хотите начать с чистого листа)

```powershell
# 1. Подключитесь к PostgreSQL
psql -U postgres

# 2. Удалите и пересоздайте БД
DROP DATABASE IF EXISTS ai_business_assistant;
CREATE DATABASE ai_business_assistant;
\q

# 3. Создайте таблицы
python -c "from database.database import init_db; init_db()"
```

---

### Шаг 3: Запустите Backend API

#### Откройте первый терминал PowerShell:

```powershell
# Активируйте виртуальное окружение
.\venv\Scripts\Activate.ps1

# Если получите ошибку ExecutionPolicy, выполните:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Запустите API
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Ожидаемый вывод**:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **API запущен!**
- API URL: http://localhost:8000
- Swagger Docs: http://localhost:8000/api/docs

---

### Шаг 4: Запустите Frontend Web App

#### Откройте второй терминал PowerShell:

```powershell
# Перейдите в папку web-app
cd web-app

# Запустите dev server
npm run dev
```

**Ожидаемый вывод**:
```
  VITE v5.x.x  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ **Web App запущен!**
- Web App URL: http://localhost:5173

---

## 🧪 Тестирование

### 1. Откройте браузер

Перейдите на **http://localhost:5173**

### 2. Регистрация

1. Нажмите вкладку **"Sign Up"**
2. Заполните:
   - **Username**: demo
   - **Password**: Demo123456
   - **Email**: demo@example.com
3. Нажмите **"Sign Up"**

✅ Вы должны автоматически войти на Dashboard

### 3. Загрузите документ

1. **Documents** → **Select File** → выберите любой файл
2. Нажмите **Upload**
3. Дождитесь 100%
4. Нажмите **Activate**

### 4. Протестируйте AI Chat

1. **Chat** → введите "What is this document about?"
2. Нажмите Enter
3. AI ответит через 2-5 секунд

---

## 🐛 Troubleshooting

### Ошибка: "Cannot connect to database"

**Решение**:
1. Убедитесь что PostgreSQL запущен
2. Проверьте `.env` файл - правильный ли пароль?
3. Проверьте DATABASE_URL

```powershell
# Проверьте статус PostgreSQL
Get-Service -Name postgresql*

# Если не запущен:
Start-Service postgresql-x64-14  # Замените на вашу версию
```

---

### Ошибка: "Port 8000 already in use"

**Решение**:
```powershell
# Найдите процесс на порту 8000
netstat -ano | findstr :8000

# Убейте процесс (замените PID на найденный номер)
taskkill /PID <PID> /F
```

---

### Ошибка: "GEMINI_API_KEY not found"

**Решение**:
1. Получите API key: https://makersuite.google.com/app/apikey
2. Добавьте в `.env`:
   ```
   GEMINI_API_KEY=your-actual-api-key-here
   ```
3. Перезапустите API server

---

### Ошибка: ExecutionPolicy при активации venv

**Решение**:
```powershell
# Разрешите запуск скриптов для текущего пользователя
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Затем снова активируйте venv
.\venv\Scripts\Activate.ps1
```

---

### Ошибка: "ModuleNotFoundError"

**Решение**:
```powershell
# Активируйте venv
.\venv\Scripts\Activate.ps1

# Установите все зависимости
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose passlib bcrypt python-multipart google-generativeai alembic python-dotenv
```

---

## 📝 Полезные команды

### Backend

```powershell
# Активировать venv
.\venv\Scripts\Activate.ps1

# Установить зависимости
pip install -r requirements.txt

# Запустить API
uvicorn api.main:app --reload --port 8000

# Проверить здоровье API
Invoke-WebRequest -Uri http://localhost:8000/health
```

### Frontend

```powershell
# Перейти в web-app
cd web-app

# Установить зависимости
npm install

# Запустить dev server
npm run dev

# Собрать для production
npm run build

# Просмотреть production build
npm run preview
```

### Database

```powershell
# Подключиться к PostgreSQL
psql -U postgres

# Список баз данных
\l

# Подключиться к БД
\c ai_business_assistant

# Список таблиц
\dt

# Выйти
\q
```

---

## ✅ Чек-лист готовности

Перед запуском убедитесь:

- [ ] PostgreSQL установлен и запущен
- [ ] Python 3.10+ установлен
- [ ] Node.js 18+ и npm установлены
- [ ] Создан `.env` файл с правильными данными
- [ ] Виртуальное окружение создано (`python -m venv venv`)
- [ ] Python зависимости установлены (`pip install ...`)
- [ ] Node.js зависимости установлены (`cd web-app && npm install`)
- [ ] База данных создана (`CREATE DATABASE ai_business_assistant`)
- [ ] Таблицы созданы (уже есть или запустить `init_db()`)
- [ ] Gemini API key получен и добавлен в `.env`

---

## 🎯 Следующие шаги

После успешного запуска:

1. ✅ **Протестируйте все функции** (регистрация, документы, чат, аналитика)
2. ✅ **Проверьте API docs** на http://localhost:8000/api/docs
3. ✅ **Откройте DevTools (F12)** и следите за Console
4. ✅ **Попробуйте разные типы документов** (PDF, Excel, Word)
5. ✅ **Задавайте вопросы AI** и проверяйте ответы

---

## 📞 Поддержка

Если проблемы остались:

1. Проверьте логи в терминале (Backend и Frontend)
2. Откройте DevTools → Console в браузере
3. Проверьте `.env` файл
4. Убедитесь что PostgreSQL запущен
5. Создайте Issue на GitHub: https://github.com/kandibobe/ai-business-asistant/issues

---

**Готово! Теперь всё должно работать! 🚀**

Удачи с разработкой! 🎉
