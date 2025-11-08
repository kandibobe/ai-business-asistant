# celery_app.py
import os
import sys
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

# Создаем экземпляр Celery
# Первый аргумент - имя текущего модуля.
# broker - URL нашего Redis сервера.
app = Celery(
    'worker',
    broker=os.getenv('REDIS_URL'),
    include=['tasks'] # Указываем, где искать задачи (tasks.py в корне)
)

# Конфигурация для Windows (исправление PermissionError с billiard)
if sys.platform == 'win32':
    app.conf.update(
        worker_pool='solo',  # Использовать solo pool вместо prefork на Windows
        task_track_started=True,
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        broker_connection_retry_on_startup=True,  # Исправление для Celery 6.0+
    )
else:
    app.conf.update(
        task_track_started=True,
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        broker_connection_retry_on_startup=True,
    )

# Эта настройка позволяет Celery автоматически находить задачи
# в файлах с именем tasks.py внутри приложений.
app.autodiscover_tasks()