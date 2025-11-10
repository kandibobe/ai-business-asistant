#!/usr/bin/env python3
"""
Проверка настройки проекта AI Business Assistant.
Проверяет все зависимости и сервисы.

Использование:
    python check_setup.py
"""
import sys
import os

def check_python_magic():
    """Проверка python-magic."""
    try:
        import magic
        print("✅ python-magic: OK")
        return True
    except ImportError:
        print("❌ python-magic: Not installed")
        print("   Fix: pip install python-magic-bin")
        return False

def check_ffmpeg():
    """Проверка ffmpeg."""
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True,
                              timeout=5)
        if result.returncode == 0:
            print("✅ ffmpeg: OK")
            return True
        else:
            print("❌ ffmpeg: Found but not working")
            return False
    except FileNotFoundError:
        print("❌ ffmpeg: Not found")
        print("   Fix (Windows): choco install ffmpeg")
        print("   Fix (Linux): sudo apt-get install ffmpeg")
        print("   Fix (Mac): brew install ffmpeg")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  ffmpeg: Timeout (but probably works)")
        return True

def check_redis():
    """Проверка Redis."""
    try:
        import redis
        from dotenv import load_dotenv
        load_dotenv()

        redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        r = redis.from_url(redis_url, socket_timeout=2)
        r.ping()
        print(f"✅ Redis: OK ({redis_url})")
        return True
    except ImportError:
        print("❌ Redis: redis package not installed")
        print("   Fix: pip install redis")
        return False
    except Exception as e:
        print(f"❌ Redis: Not available ({str(e)})")
        print("   Fix: docker-compose up -d")
        return False

def check_postgresql():
    """Проверка PostgreSQL."""
    try:
        import psycopg2
        from dotenv import load_dotenv
        load_dotenv()

        conn_params = {
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASS'),
            'database': os.getenv('DB_NAME'),
            'connect_timeout': 3
        }

        if not all([conn_params['host'], conn_params['user'], conn_params['database']]):
            print("❌ PostgreSQL: .env not configured")
            print("   Fix: Copy .env.example to .env and fill in values")
            return False

        conn = psycopg2.connect(**conn_params)
        conn.close()
        print(f"✅ PostgreSQL: OK ({conn_params['host']}:{conn_params['port']})")
        return True
    except ImportError:
        print("❌ PostgreSQL: psycopg2 not installed")
        print("   Fix: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ PostgreSQL: Not available ({str(e)})")
        print("   Fix: docker-compose up -d")
        return False

def check_psutil():
    """Проверка psutil."""
    try:
        import psutil
        print("✅ psutil: OK (for system monitoring)")
        return True
    except ImportError:
        print("⚠️  psutil: Not installed (optional, for health checks)")
        print("   Fix: pip install psutil")
        return True  # Not critical

def check_env_file():
    """Проверка .env файла."""
    if not os.path.exists('.env'):
        print("❌ .env file: Not found")
        print("   Fix: Copy .env.example to .env")
        print("   Command: copy .env.example .env")
        return False

    from dotenv import load_dotenv
    load_dotenv()

    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'GEMINI_API_KEY',
        'DB_HOST',
        'DB_USER',
        'DB_PASS',
        'DB_NAME',
    ]

    missing = []
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == f'your_{var.lower()}_here':
            missing.append(var)

    if missing:
        print(f"❌ .env file: Missing variables: {', '.join(missing)}")
        print("   Fix: Edit .env and fill in actual values")
        return False

    print("✅ .env file: OK (all required variables set)")
    return True

def check_new_improvements():
    """Проверка новых файлов улучшений."""
    new_files = [
        'utils/health_check.py',
        'utils/metrics.py',
    ]

    all_exist = True
    for file in new_files:
        if os.path.exists(file):
            print(f"✅ {file}: Exists")
        else:
            print(f"❌ {file}: Missing")
            all_exist = False

    if not all_exist:
        print("   Fix: Run 'python apply_improvements.py'")

    return all_exist

def check_docker():
    """Проверка Docker."""
    import subprocess
    try:
        result = subprocess.run(['docker', 'ps'],
                              capture_output=True,
                              timeout=5)
        if result.returncode == 0:
            print("✅ Docker: Running")

            # Проверяем docker-compose
            try:
                result = subprocess.run(['docker-compose', 'ps'],
                                      capture_output=True,
                                      timeout=5,
                                      cwd=os.getcwd())
                output = result.stdout.decode('utf-8', errors='ignore')

                # Проверяем что PostgreSQL и Redis запущены
                postgres_running = 'postgres' in output.lower() and 'up' in output.lower()
                redis_running = 'redis' in output.lower() and 'up' in output.lower()

                if postgres_running and redis_running:
                    print("   ✅ docker-compose services: Running (PostgreSQL + Redis)")
                else:
                    print("   ⚠️  docker-compose services: Not all services running")
                    print("       Fix: docker-compose up -d")

            except FileNotFoundError:
                print("   ⚠️  docker-compose: Not found")

            return True
    except FileNotFoundError:
        print("⚠️  Docker: Not found (using external DB/Redis?)")
        return True  # Not critical if using external services
    except subprocess.TimeoutExpired:
        print("⚠️  Docker: Timeout")
        return True

if __name__ == "__main__":
    print("=" * 70)
    print("🔍 Проверка настройки AI Business Assistant")
    print("=" * 70)
    print()

    print("📦 Зависимости:")
    print("-" * 70)
    dep_results = [
        check_python_magic(),
        check_ffmpeg(),
        check_psutil(),
    ]

    print()
    print("📄 Конфигурация:")
    print("-" * 70)
    config_results = [
        check_env_file(),
        check_new_improvements(),
    ]

    print()
    print("🐳 Инфраструктура:")
    print("-" * 70)
    infra_results = [
        check_docker(),
        check_redis(),
        check_postgresql(),
    ]

    print()
    print("=" * 70)

    # Подсчет результатов
    all_results = dep_results + config_results + infra_results
    passed = sum(all_results)
    total = len(all_results)

    critical_results = config_results + [infra_results[1], infra_results[2]]  # .env, redis, postgres
    critical_passed = sum(critical_results)
    critical_total = len(critical_results)

    print(f"📊 Общий результат: {passed}/{total} проверок пройдено")

    if critical_passed == critical_total:
        print("✅ Все критические компоненты готовы!")
        print()
        print("🚀 Можно запускать:")
        print("   python main.py              # Telegram bot")
        print("   uvicorn api.main:app        # REST API")
        print("   celery -A celery_app worker # Background tasks")
        print()

        if passed < total:
            print("💡 Некритичные предупреждения:")
            if not dep_results[0]:  # python-magic
                print("   - python-magic: Работа с файлами будет ограничена")
            if not dep_results[1]:  # ffmpeg
                print("   - ffmpeg: Аудио сообщения не будут работать")
            if not dep_results[2]:  # psutil
                print("   - psutil: Системная статистика будет недоступна")
            print()

        sys.exit(0)
    else:
        print("❌ Не все критические компоненты готовы")
        print()
        print("🔧 Исправьте ошибки выше перед запуском")
        print("📖 См. FIX_WARNINGS.md для подробных инструкций")
        print()
        sys.exit(1)
