# handlers/audio.py

import os
from telegram import Update
from telegram.ext import ContextTypes

# Импортируем нашу новую задачу для аудио
from .tasks import transcribe_audio_task

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Обрабатывает загрузку аудиофайла или голосового сообщения.
    """
    user = update.effective_user
    
    if update.message.audio:
        audio_file = update.message.audio
        file_name = audio_file.file_name or "audio.mp3"
    elif update.message.voice:
        audio_file = update.message.voice
        file_name = "voice_message.ogg"
    else:
        return

    new_file = await context.bot.get_file(audio_file.file_id)
    
    file_path = os.path.join(DOWNLOAD_DIR, f"{user.id}_{file_name}")
    await new_file.download_to_drive(file_path)
    
    await update.message.reply_text(
        f"✅ Аудиофайл '{file_name}' принят в работу! "
        "Начинаю транскрибацию. Это может занять некоторое время... Уведомлю о готовности."
    )
    
    # Ставим задачу транскрибации в очередь Celery
    transcribe_audio_task.delay(
        chat_id=update.message.chat_id,
        user_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        file_path=file_path,
        file_name=file_name
    )