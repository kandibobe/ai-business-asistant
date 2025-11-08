# handlers/documents.py

import os
from telegram import Update
from telegram.ext import ContextTypes

# Импортируем нашу новую задачу из tasks.py в корне проекта
from tasks import process_pdf_task

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает загрузку PDF-файла.
    1. Быстро скачивает файл.
    2. Мгновенно отвечает пользователю.
    3. Ставит "тяжелую" задачу по обработке в очередь Celery.
    """
    user = update.effective_user
    
    if not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл.")
        return

    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    new_file = await context.bot.get_file(file_id)
    
    # Сохраняем файл с уникальным именем, чтобы избежать конфликтов
    file_path = os.path.join(DOWNLOAD_DIR, f"{user.id}_{file_name}")
    await new_file.download_to_drive(file_path)
    
    # --- КЛЮЧЕВОЕ ИЗМЕНЕНИЕ ---
    # 1. Мгновенно отвечаем пользователю
    await update.message.reply_text(
        f"✅ Файл '{file_name}' принят в работу! "
        "Уведомлю, как только анализ будет готов."
    )
    
    # 2. Вызываем нашу асинхронную задачу
    # .delay() - это стандартный способ запуска задачи Celery
    process_pdf_task.delay(
        chat_id=update.message.chat_id,
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        file_path=file_path,
        file_name=file_name
    )