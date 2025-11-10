# 🎯 HOW TO START - Краткая инструкция

## ✅ Frontend уже запущен!

Ваш frontend работает на: **http://localhost:3000/** ✅

---

## ❌ Проблема: API не запускается

**Ошибка**: `ModuleNotFoundError: No module named 'api'`

**Причина**: Вы запустили API из папки `web-app`, а нужно из корня проекта!

---

## 🔧 РЕШЕНИЕ: Запустите API из корня проекта

### Откройте НОВЫЙ терминал PowerShell

1. **Закройте текущий терминал с ошибкой** (Ctrl+C)
2. **Откройте новый PowerShell**
3. **Перейдите в КОРЕНЬ проекта** (не в web-app!)

```powershell
# Перейдите в корень проекта (выйдите из web-app)
cd "C:\demo fiverr"

# Убедитесь что вы в правильной папке - должны видеть папку api/
ls
```

Вы должны увидеть папки: `api/`, `web-app/`, `database/`, `utils/` и т.д.

---

### Активируйте виртуальное окружение

```powershell
# Активируйте venv
.\.venv\Scripts\Activate.ps1

# Если ошибка ExecutionPolicy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Затем снова:
.\.venv\Scripts\Activate.ps1
```

---

### Убедитесь что есть файл `.env`

```powershell
# Проверьте наличие .env
cat .env

# Если файла нет, создайте его:
@"
DATABASE_URL=postgresql://postgres:ваш_пароль@localhost:5432/ai_business_assistant
JWT_SECRET=your-super-secret-key-change-me-in-production-12345
GEMINI_API_KEY=ваш-gemini-api-key
"@ | Out-File -FilePath .env -Encoding UTF8
```

**ВАЖНО**: Замените:
- `ваш_пароль` - на пароль PostgreSQL
- `ваш-gemini-api-key` - на ключ с https://makersuite.google.com/app/apikey

---

### Запустите API

```powershell
# ИЗ КОРНЯ ПРОЕКТА (не из web-app!)
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Или используйте готовый скрипт**:
```powershell
.\start_windows.ps1
```

---

## ✅ Ожидаемый результат

После запуска API вы должны увидеть:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using StatReload
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## 🌐 Откройте в браузере

Теперь откройте: **http://localhost:3000**

Вы должны увидеть страницу входа/регистрации!

---

## 📋 Чек-лист

- [ ] Закрыл терминал с ошибкой API
- [ ] Открыл новый PowerShell
- [ ] Перешёл в корень проекта `cd "C:\demo fiverr"`
- [ ] Проверил что вижу папку `api/` (командой `ls`)
- [ ] Активировал venv: `.\.venv\Scripts\Activate.ps1`
- [ ] Создал `.env` файл с правильными данными
- [ ] Запустил API: `uvicorn api.main:app --reload --port 8000`
- [ ] Вижу "Application startup complete" ✅
- [ ] Открыл http://localhost:3000 в браузере
- [ ] Frontend загрузился ✅

---

## 🎯 Структура терминалов

**Терминал 1 (PowerShell)** - Backend API:
```
C:\demo fiverr> .\.venv\Scripts\Activate.ps1
C:\demo fiverr> uvicorn api.main:app --reload --port 8000
```

**Терминал 2 (PowerShell)** - Frontend (уже работает!):
```
C:\demo fiverr\web-app> npm run dev
✅ VITE v7.2.2 ready in 490 ms
➜ Local: http://localhost:3000/
```

---

## ❓ Если всё равно не работает

### Ошибка: "Cannot connect to database"
```powershell
# Проверьте что PostgreSQL запущен
Get-Service postgresql*

# Если не запущен:
Start-Service postgresql-x64-14  # Замените на вашу версию
```

### Ошибка: "GEMINI_API_KEY not set"
1. Получите ключ: https://makersuite.google.com/app/apikey
2. Добавьте в `.env`: `GEMINI_API_KEY=ваш-ключ`
3. Перезапустите API (Ctrl+C, затем снова uvicorn)

### Ошибка: "Port 8000 already in use"
```powershell
# Найдите процесс
netstat -ano | findstr :8000

# Убейте процесс (замените PID)
taskkill /PID <номер> /F
```

---

## 📚 Дополнительная документация

- **WINDOWS_SETUP.md** - Полное руководство для Windows
- **START_HERE.md** - Быстрый старт
- **QUICKSTART.md** - Подробное руководство

---

**Главное правило**: API запускается из КОРНЯ проекта (`C:\demo fiverr`), НЕ из `web-app`! 🎯
