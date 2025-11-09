# handlers/documents.py

import os
from telegram import Update
from telegram.ext import ContextTypes

# Импортируем все задачи обработки документов
from tasks import process_pdf_task, process_excel_task, process_word_task

# Импортируем систему безопасности
from utils.security import validate_file, get_safe_file_path, FileValidationError
from middleware.rate_limiter import rate_limit, RateLimitExceeded

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@rate_limit('document_upload')
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Универсальный обработчик для различных типов документов.
    Поддерживает: PDF, Excel (.xlsx, .xls), Word (.docx)

    1. Быстро скачивает файл.
    2. Определяет тип файла по расширению.
    3. Валидирует файл (размер, тип, безопасность).
    4. Мгновенно отвечает пользователю.
    5. Ставит соответствующую задачу в очередь Celery.
    """
    user = update.effective_user

    if not update.message.document:
        await update.message.reply_text("Пожалуйста, отправьте файл.")
        return

    file_id = update.message.document.file_id
    file_name = update.message.document.file_name
    file_size = update.message.document.file_size

    # Базовая проверка размера до скачивания
    max_size = 50 * 1024 * 1024  # 50 MB общий лимит
    if file_size and file_size > max_size:
        await update.message.reply_text(
            f"❌ Файл слишком большой: {file_size / (1024*1024):.2f} MB\n"
            f"Максимальный размер: {max_size / (1024*1024):.2f} MB"
        )
        return

    new_file = await context.bot.get_file(file_id)

    # Создаем безопасный путь для файла
    file_path = get_safe_file_path(DOWNLOAD_DIR, user.id, file_name)

    try:
        await new_file.download_to_drive(file_path)
    except Exception as e:
        await update.message.reply_text(
            f"❌ Ошибка при загрузке файла: {str(e)}\n"
            "Попробуйте еще раз или свяжитесь с поддержкой."
        )
        return

    # Определяем тип файла по расширению
    file_extension = os.path.splitext(file_name)[1].lower()

    # Словарь: расширение -> (задача Celery, эмодзи, описание типа, тип для валидации)
    file_handlers = {
        '.pdf': (process_pdf_task, '📄', 'PDF', 'pdf'),
        '.xlsx': (process_excel_task, '📊', 'Excel', 'excel'),
        '.xls': (process_excel_task, '📊', 'Excel', 'excel'),
        '.docx': (process_word_task, '📝', 'Word', 'word'),
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

    task, emoji, file_type, validation_type = file_handlers[file_extension]

    # БЕЗОПАСНОСТЬ: Валидация файла
    try:
        is_valid, error_msg = validate_file(file_path, file_name, validation_type)
        if not is_valid:
            await update.message.reply_text(
                f"❌ Файл не прошел проверку безопасности:\n{error_msg}\n\n"
                "Убедитесь, что файл не поврежден и имеет корректный формат."
            )
            # Удаляем невалидный файл
            if os.path.exists(file_path):
                os.remove(file_path)
            return
    except FileValidationError as e:
        await update.message.reply_text(
            f"❌ Ошибка валидации файла:\n{str(e)}"
        )
        if os.path.exists(file_path):
            os.remove(file_path)
        return
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ Не удалось проверить файл: {str(e)}\n"
            "Файл будет обработан, но рекомендуем проверить его корректность."
        )

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