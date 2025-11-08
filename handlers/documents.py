# handlers/documents.py

import os
from telegram import Update
from telegram.ext import ContextTypes

# Импортируем все задачи обработки документов
from tasks import process_pdf_task, process_excel_task, process_word_task

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Универсальный обработчик для различных типов документов.
    Поддерживает: PDF, Excel (.xlsx, .xls), Word (.docx)

    1. Быстро скачивает файл.
    2. Определяет тип файла по расширению.
    3. Мгновенно отвечает пользователю.
    4. Ставит соответствующую задачу в очередь Celery.
    """
    user = update.effective_user

    if not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл.")
        return

    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    new_file = await context.bot.get_file(file_id)

    # Сохраняем файл с уникальным именем
    file_path = os.path.join(DOWNLOAD_DIR, f"{user.id}_{file_name}")
    await new_file.download_to_drive(file_path)

    # Определяем тип файла по расширению
    file_extension = os.path.splitext(file_name)[1].lower()

    # Словарь: расширение -> (задача Celery, эмодзи, описание типа)
    file_handlers = {
        '.pdf': (process_pdf_task, '📄', 'PDF'),
        '.xlsx': (process_excel_task, '📊', 'Excel'),
        '.xls': (process_excel_task, '📊', 'Excel'),
        '.docx': (process_word_task, '📝', 'Word'),
    }

    if file_extension not in file_handlers:
        await update.message.reply_text(
            f"❌ Неподдерживаемый формат файла: {file_extension}\n\n"
            "Поддерживаемые форматы:\n"
            "📄 PDF (.pdf)\n"
            "📊 Excel (.xlsx, .xls)\n"
            "📝 Word (.docx)"
        )
        # Удаляем неподдерживаемый файл
        if os.path.exists(file_path):
            os.remove(file_path)
        return

    task, emoji, file_type = file_handlers[file_extension]

    # Мгновенно отвечаем пользователю
    await update.message.reply_text(
        f"{emoji} Файл '{file_name}' ({file_type}) принят в работу!\n"
        "Начинаю анализ... Уведомлю о готовности."
    )

    # Вызываем соответствующую асинхронную задачу
    task.delay(
        chat_id=update.message.chat_id,
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        file_path=file_path,
        file_name=file_name
    )