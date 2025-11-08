# celery_app.py
import os
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

# Эта настройка позволяет Celery автоматически находить задачи
# в файлах с именем tasks.py внутри приложений.
app.autodiscover_tasks()