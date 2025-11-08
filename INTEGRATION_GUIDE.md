# 🌍 Multilingual Support & UI Improvements - Integration Guide

## 📁 Новые файлы созданы:

1. **`config/i18n.py`** - Модуль локализации (3 языка: RU, EN, DE)
2. **`ui/reply_keyboards.py`** - Постоянные клавиатуры внизу экрана
3. **`handlers/reply_keyboard_handler.py`** - Обработчик кнопок быстрого доступа
4. **`migrate_language.py`** - Миграция для добавления поля language в БД

## 🔧 Требуемые изменения в существующих файлах:

### 1. **main.py** - Добавить регистрацию нового обработчика

```python
# После импортов добавить:
from handlers.reply_keyboard_handler import handle_reply_keyboard
from migrate_language import migrate_language_field

# В функции main() после init_db() добавить:
migrate_language_field()  # Запускаем миграцию языков

# Перед регистрацией MessageHandler для текстовых сообщений добавить:
# Обработчик для кнопок быстрого доступа (ReplyKeyboard)
async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Сначала проверяем, не является ли это командой от ReplyKeyboard
    if await handle_reply_keyboard(update, context):
        return
    # Если нет, обрабатываем как обычное сообщение
    await message_handler_with_model(update, context)

# Заменить строку:
# application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler_with_model))
# На:
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message_handler))
```

### 2. **handlers/common_enhanced.py** - Добавить ReplyKeyboard в start()

```python
# В функции start() добавить импорт:
from ui import get_main_reply_keyboard

# Изменить reply_html чтобы включить ReplyKeyboard:
if update.message:
    await update.message.reply_html(
        welcome_text,
        reply_markup=get_main_menu_keyboard()
    )
    # Отправляем вторым сообщением ReplyKeyboard
    await update.message.reply_text(
        "Используйте кнопки внизу для быстрого доступа ⬇️",
        reply_markup=get_main_reply_keyboard(lang='ru')  # TODO: использовать язык из БД
    )
```

### 3. **fix_and_start.bat** - Добавить миграцию языков

```batch
REM После строки "python migrate_user_preferences.py" добавить:
echo [5c] Миграция языков...
python migrate_language.py
if %ERRORLEVEL% neq 0 (
    echo [ОШИБКА] Миграция языков не удалась
    goto error
)
```

## 🎨 Использование i18n в коде:

```python
from config.i18n import get_text

# В любом handler:
user_lang = db_user.language or 'ru'
message = get_text('welcome_new', user_lang, name=user.first_name)
```

## 🔤 Доступные ключи переводов:

- `welcome_new` - Приветствие для нового пользователя
- `welcome_back` - Приветствие для вернувшегося пользователя
- `btn_my_docs` - Кнопка "Мои документы"
- `btn_stats` - Кнопка "Статистика"
- `btn_dev_tools` - Кнопка "Developer Tools"
- `btn_ai_chat` - Кнопка "AI Chat"
- `btn_settings` - Кнопка "Настройки"
- `btn_help` - Кнопка "Помощь"
- ... и много других (см. config/i18n.py)

## 🎯 Основные функции:

### get_text(key, lang, **kwargs)
Получает переведенный текст с поддержкой форматирования:
```python
text = get_text('doc_uploaded', 'en', filename='test.pdf', size='1.5 MB', words=1000)
```

### get_main_reply_keyboard(lang)
Создает главную постоянную клавиатуру:
```python
keyboard = get_main_reply_keyboard('ru')
await message.reply_text("Текст", reply_markup=keyboard)
```

## ✅ После интеграции:

1. Запустить `python migrate_language.py` вручную ИЛИ через fix_and_start.bat
2. Перезапустить бота
3. Проверить что кнопки внизу появились
4. Проверить переключение языка в настройках

## 🚀 Следующие шаги для полной интеграции:

1. Обновить все handlers чтобы использовать `get_text()` вместо жестко закодированных строк
2. Добавить переключатель языка в меню настроек
3. Сохранять выбранный язык в БД при переключении
4. Обновить все inline-клавиатуры чтобы учитывать язык пользователя

## 📝 Примечания:

- ReplyKeyboard видна всегда внизу экрана (удобно!)
- Inline клавиатуры (кнопки под сообщениями) остаются без изменений
- Язык по умолчанию: Русский (ru)
- Поддерживаемые языки: 🇷🇺 Русский, 🇬🇧 English, 🇩🇪 Deutsch
