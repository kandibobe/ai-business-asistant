# ==============================================================================
# Quick Start Guide for Windows Users
# ==============================================================================

## 🪟 Windows Setup

На Windows используйте PowerShell скрипты вместо `make`:

### Основные команды

```powershell
# Показать все доступные команды
.\dev.ps1 help

# Запустить development окружение
.\dev.ps1 dev

# Посмотреть логи
.\dev.ps1 logs

# Остановить контейнеры
.\dev.ps1 stop
```

## 📋 Альтернатива 1: Напрямую через docker-compose

Если PowerShell скрипты не работают, используйте docker-compose напрямую:

```powershell
# Запустить development
docker-compose up -d

# Посмотреть логи
docker-compose logs -f

# Посмотреть статус
docker-compose ps

# Остановить
docker-compose down
```

## 📋 Альтернатива 2: Установить Make для Windows

### Вариант A: Chocolatey (рекомендуется)
```powershell
# Установить Chocolatey (если еще не установлен)
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Установить make
choco install make
```

### Вариант B: Git Bash
Если у вас установлен Git for Windows, используйте Git Bash:
```bash
# Открыть Git Bash и использовать обычные make команды
make dev
make logs
```

### Вариант C: WSL (Windows Subsystem for Linux)
```powershell
# Установить WSL
wsl --install

# После установки открыть WSL и использовать Linux команды
make dev
```

## 🚀 Быстрый старт (Windows)

### 1. Проверка Docker

```powershell
docker --version
docker-compose --version
```

### 2. Настройка окружения

```powershell
# Скопировать .env.example в .env
Copy-Item .env.example .env

# Отредактировать .env в любом текстовом редакторе
notepad .env
```

### 3. Запуск

```powershell
# Вариант 1: PowerShell скрипт
.\dev.ps1 dev

# Вариант 2: docker-compose напрямую
docker-compose up -d
```

### 4. Проверка

```powershell
# Посмотреть запущенные контейнеры
.\dev.ps1 ps
# или
docker-compose ps
```

### 5. Просмотр логов

```powershell
.\dev.ps1 logs
# или
docker-compose logs -f
```

## 📊 Полезные команды для Windows

### Просмотр логов конкретного сервиса
```powershell
docker-compose logs -f api    # API логи
docker-compose logs -f bot    # Bot логи
docker-compose logs -f db     # Database логи
```

### Перезапуск сервиса
```powershell
docker-compose restart api
docker-compose restart bot
```

### Открыть shell в контейнере
```powershell
docker-compose exec api /bin/bash
docker-compose exec db /bin/sh
```

### Миграции базы данных
```powershell
docker-compose exec api alembic upgrade head
```

### Создать backup базы данных
```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
docker-compose exec db sh -c "pg_dump -U $env:DB_USER $env:DB_NAME | gzip > /backups/backup_$timestamp.sql.gz"
```

### Запустить тесты
```powershell
pytest tests/ -v
```

## 🐛 Troubleshooting (Windows)

### Проблема: PowerShell блокирует выполнение скриптов

**Решение:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Проблема: Docker daemon не запущен

**Решение:**
1. Открыть Docker Desktop
2. Дождаться запуска Docker
3. Повторить команду

### Проблема: Порты уже заняты

**Решение:**
```powershell
# Проверить, что занимает порт 5432 (PostgreSQL)
netstat -ano | findstr :5432

# Проверить, что занимает порт 8000 (API)
netstat -ano | findstr :8000

# Убить процесс (замените PID на реальный ID процесса)
taskkill /PID <PID> /F
```

### Проблема: Ошибка "file not found" при docker-compose up

**Решение:**
```powershell
# Пересобрать контейнеры
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

## 📚 Дополнительные ресурсы

- [Docker для Windows](https://docs.docker.com/desktop/install/windows-install/)
- [PowerShell документация](https://docs.microsoft.com/en-us/powershell/)
- [WSL установка](https://docs.microsoft.com/en-us/windows/wsl/install)

---

**Совет:** Для лучшего опыта разработки на Windows рекомендуем использовать WSL 2 + Docker Desktop
