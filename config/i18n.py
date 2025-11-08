"""
Модуль интернационализации (i18n) для поддержки нескольких языков.
Поддерживаемые языки: Русский (ru), English (en), Deutsch (de)
"""

LANGUAGES = {
    'ru': '🇷🇺 Русский',
    'en': '🇬🇧 English',
    'de': '🇩🇪 Deutsch',
}

# Основные тексты интерфейса
TRANSLATIONS = {
    # Welcome messages
    'welcome_new': {
        'ru': '👋 Привет, <b>{name}</b>!\n\n🎉 Добро пожаловать в <b>AI Business Intelligence Agent v2.0</b>!\n\n✨ Я помогу вам:\n• 📄 Анализировать документы (PDF, Excel, Word)\n• 💬 Отвечать на вопросы по документам\n• 📊 Создавать отчеты и визуализации\n• 💻 Использовать инструменты разработчика\n• 🤖 Общаться с AI без документов\n\n💡 Начните с загрузки документа или выберите действие в меню!',
        'en': '👋 Hello, <b>{name}</b>!\n\n🎉 Welcome to <b>AI Business Intelligence Agent v2.0</b>!\n\n✨ I can help you:\n• 📄 Analyze documents (PDF, Excel, Word)\n• 💬 Answer questions about documents\n• 📊 Create reports and visualizations\n• 💻 Use developer tools\n• 🤖 Chat with AI without documents\n\n💡 Start by uploading a document or choose an action from the menu!',
        'de': '👋 Hallo, <b>{name}</b>!\n\n🎉 Willkommen bei <b>AI Business Intelligence Agent v2.0</b>!\n\n✨ Ich kann Ihnen helfen:\n• 📄 Dokumente analysieren (PDF, Excel, Word)\n• 💬 Fragen zu Dokumenten beantworten\n• 📊 Berichte und Visualisierungen erstellen\n• 💻 Entwickler-Tools verwenden\n• 🤖 Mit AI ohne Dokumente chatten\n\n💡 Laden Sie ein Dokument hoch oder wählen Sie eine Aktion aus dem Menü!',
    },
    'welcome_back': {
        'ru': '👋 С возвращением, <b>{name}</b>!\n\n🤖 Я готов помочь вам с анализом документов и ответами на вопросы.\n\n💡 Используйте кнопки ниже для быстрого доступа!',
        'en': '👋 Welcome back, <b>{name}</b>!\n\n🤖 I\'m ready to help you analyze documents and answer questions.\n\n💡 Use the buttons below for quick access!',
        'de': '👋 Willkommen zurück, <b>{name}</b>!\n\n🤖 Ich bin bereit, Ihnen bei der Dokumentenanalyse zu helfen.\n\n💡 Verwenden Sie die Schaltflächen unten für schnellen Zugriff!',
    },

    # Main menu buttons
    'btn_my_docs': {
        'ru': '📄 Мои документы',
        'en': '📄 My Documents',
        'de': '📄 Meine Dokumente',
    },
    'btn_stats': {
        'ru': '📊 Статистика',
        'en': '📊 Statistics',
        'de': '📊 Statistiken',
    },
    'btn_dev_tools': {
        'ru': '💻 Developer Tools',
        'en': '💻 Developer Tools',
        'de': '💻 Entwickler-Tools',
    },
    'btn_ai_chat': {
        'ru': '🤖 AI Chat',
        'en': '🤖 AI Chat',
        'de': '🤖 AI Chat',
    },
    'btn_settings': {
        'ru': '⚙️ Настройки',
        'en': '⚙️ Settings',
        'de': '⚙️ Einstellungen',
    },
    'btn_help': {
        'ru': '❓ Помощь',
        'en': '❓ Help',
        'de': '❓ Hilfe',
    },
    'btn_language': {
        'ru': '🌐 Язык',
        'en': '🌐 Language',
        'de': '🌐 Sprache',
    },
    'btn_premium': {
        'ru': '💎 Premium',
        'en': '💎 Premium',
        'de': '💎 Premium',
    },
    'btn_back': {
        'ru': '⬅️ Назад',
        'en': '⬅️ Back',
        'de': '⬅️ Zurück',
    },
    'btn_cancel': {
        'ru': '❌ Отмена',
        'en': '❌ Cancel',
        'de': '❌ Abbrechen',
    },
    'btn_main_menu': {
        'ru': '🏠 Главное меню',
        'en': '🏠 Main Menu',
        'de': '🏠 Hauptmenü',
    },

    # Quick access buttons (ReplyKeyboard)
    'quick_upload': {
        'ru': '📤 Загрузить',
        'en': '📤 Upload',
        'de': '📤 Hochladen',
    },
    'quick_docs': {
        'ru': '📚 Документы',
        'en': '📚 Documents',
        'de': '📚 Dokumente',
    },
    'quick_chat': {
        'ru': '💬 Чат',
        'en': '💬 Chat',
        'de': '💬 Chat',
    },
    'quick_tools': {
        'ru': '🔧 Инструменты',
        'en': '🔧 Tools',
        'de': '🔧 Werkzeuge',
    },

    # Document messages
    'no_docs': {
        'ru': 'У вас еще нет документов.\n\n📤 Отправьте мне файл (PDF, Excel, Word) для начала работы!',
        'en': 'You don\'t have any documents yet.\n\n📤 Send me a file (PDF, Excel, Word) to get started!',
        'de': 'Sie haben noch keine Dokumente.\n\n📤 Senden Sie mir eine Datei (PDF, Excel, Word), um zu beginnen!',
    },
    'doc_uploaded': {
        'ru': '✅ Документ успешно загружен!\n\n📄 <b>{filename}</b>\n💾 Размер: {size}\n📝 Слов: {words}\n\n💡 Теперь можете задавать вопросы по документу!',
        'en': '✅ Document uploaded successfully!\n\n📄 <b>{filename}</b>\n💾 Size: {size}\n📝 Words: {words}\n\n💡 Now you can ask questions about the document!',
        'de': '✅ Dokument erfolgreich hochgeladen!\n\n📄 <b>{filename}</b>\n💾 Größe: {size}\n📝 Wörter: {words}\n\n💡 Jetzt können Sie Fragen zum Dokument stellen!',
    },
    'processing_doc': {
        'ru': '⏳ Обрабатываю документ...\n\nЭто может занять некоторое время.',
        'en': '⏳ Processing document...\n\nThis may take a moment.',
        'de': '⏳ Dokument wird verarbeitet...\n\nDies kann einen Moment dauern.',
    },
    'no_active_doc': {
        'ru': 'У вас не выбран активный документ.\n\n📚 Выберите документ из списка или загрузите новый.\n💡 Или используйте <b>🤖 AI Chat</b> для общения без документов!',
        'en': 'You don\'t have an active document selected.\n\n📚 Choose a document from the list or upload a new one.\n💡 Or use <b>🤖 AI Chat</b> to chat without documents!',
        'de': 'Sie haben kein aktives Dokument ausgewählt.\n\n📚 Wählen Sie ein Dokument aus der Liste oder laden Sie ein neues hoch.\n💡 Oder verwenden Sie <b>🤖 AI Chat</b> zum Chatten ohne Dokumente!',
    },

    # AI responses
    'thinking': {
        'ru': '🧠 Думаю над вашим вопросом...',
        'en': '🧠 Thinking about your question...',
        'de': '🧠 Denke über Ihre Frage nach...',
    },
    'ai_error': {
        'ru': '❌ Произошла ошибка при обращении к AI.\n\nПожалуйста, попробуйте еще раз.',
        'en': '❌ An error occurred while contacting the AI.\n\nPlease try again.',
        'de': '❌ Beim Kontakt mit der KI ist ein Fehler aufgetreten.\n\nBitte versuchen Sie es erneut.',
    },

    # Settings
    'settings_title': {
        'ru': '⚙️ <b>Настройки</b>\n\nВыберите параметр для изменения:',
        'en': '⚙️ <b>Settings</b>\n\nSelect a parameter to change:',
        'de': '⚙️ <b>Einstellungen</b>\n\nWählen Sie einen Parameter zum Ändern:',
    },
    'language_changed': {
        'ru': '✅ Язык изменен на <b>Русский</b>',
        'en': '✅ Language changed to <b>English</b>',
        'de': '✅ Sprache geändert auf <b>Deutsch</b>',
    },
    'select_language': {
        'ru': '🌐 <b>Выберите язык интерфейса:</b>',
        'en': '🌐 <b>Select interface language:</b>',
        'de': '🌐 <b>Wählen Sie die Sprache der Benutzeroberfläche:</b>',
    },

    # Developer Tools
    'dev_tools_menu': {
        'ru': '💻 <b>Developer Tools</b>\n\nНабор инструментов для разработчиков:\n\n🛠️ <b>Утилиты</b> - JSON, Base64, Hash, UUID, Regex\n💻 <b>Форматтеры</b> - форматирование кода\n🔐 <b>Генераторы</b> - UUID, пароли, хеши\n🔌 <b>Интеграции</b> - GitHub, NPM, Crypto\n\n💡 Все инструменты бесплатные!',
        'en': '💻 <b>Developer Tools</b>\n\nDeveloper toolkit:\n\n🛠️ <b>Utilities</b> - JSON, Base64, Hash, UUID, Regex\n💻 <b>Formatters</b> - code formatting\n🔐 <b>Generators</b> - UUID, passwords, hashes\n🔌 <b>Integrations</b> - GitHub, NPM, Crypto\n\n💡 All tools are free!',
        'de': '💻 <b>Entwickler-Tools</b>\n\nEntwickler-Toolkit:\n\n🛠️ <b>Dienstprogramme</b> - JSON, Base64, Hash, UUID, Regex\n💻 <b>Formatierer</b> - Code-Formatierung\n🔐 <b>Generatoren</b> - UUID, Passwörter, Hashes\n🔌 <b>Integrationen</b> - GitHub, NPM, Crypto\n\n💡 Alle Tools sind kostenlos!',
    },
    'dev_utilities': {
        'ru': 'Утилиты',
        'en': 'Utilities',
        'de': 'Dienstprogramme',
    },
    'dev_formatters': {
        'ru': 'Форматтеры',
        'en': 'Formatters',
        'de': 'Formatierer',
    },
    'dev_generators': {
        'ru': 'Генераторы',
        'en': 'Generators',
        'de': 'Generatoren',
    },
    'dev_integrations': {
        'ru': 'Интеграции',
        'en': 'Integrations',
        'de': 'Integrationen',
    },

    # AI Chat Mode
    'ai_chat_title': {
        'ru': '🤖 <b>AI Chat Mode</b>\n\nРежим свободного общения с AI без документов.\n\n<b>Текущие настройки:</b>\n🎭 Роль: {role}\n📝 Стиль: {style}\n\n💬 Просто напишите свой вопрос в чат!\n\n<i>Примеры:</i>\n• Объясни async/await в Python\n• Как работает REST API?\n• Лучшие практики для Git',
        'en': '🤖 <b>AI Chat Mode</b>\n\nFree conversation with AI without documents.\n\n<b>Current settings:</b>\n🎭 Role: {role}\n📝 Style: {style}\n\n💬 Just write your question in the chat!\n\n<i>Examples:</i>\n• Explain async/await in Python\n• How does REST API work?\n• Best practices for Git',
        'de': '🤖 <b>AI Chat-Modus</b>\n\nFreie Konversation mit KI ohne Dokumente.\n\n<b>Aktuelle Einstellungen:</b>\n🎭 Rolle: {role}\n📝 Stil: {style}\n\n💬 Schreiben Sie einfach Ihre Frage in den Chat!\n\n<i>Beispiele:</i>\n• Erkläre async/await in Python\n• Wie funktioniert REST API?\n• Best Practices für Git',
    },

    # Statistics
    'stats_title': {
        'ru': '📊 <b>Статистика</b>',
        'en': '📊 <b>Statistics</b>',
        'de': '📊 <b>Statistiken</b>',
    },
    'no_stats': {
        'ru': '📊 Статистика недоступна.\n\nНачните использовать бота!',
        'en': '📊 Statistics not available.\n\nStart using the bot!',
        'de': '📊 Statistiken nicht verfügbar.\n\nFangen Sie an, den Bot zu benutzen!',
    },

    # Help
    'help_title': {
        'ru': '❓ <b>Помощь</b>\n\n<b>Основные команды:</b>\n/start - Главное меню\n/mydocs - Мои документы\n/stats - Статистика\n/settings - Настройки\n/help - Эта справка\n\n<b>Как использовать:</b>\n1️⃣ Загрузите документ (PDF, Excel, Word)\n2️⃣ Задавайте вопросы по документу\n3️⃣ Используйте Developer Tools\n4️⃣ Общайтесь с AI без документов\n\n💡 Используйте кнопки внизу экрана для быстрого доступа!',
        'en': '❓ <b>Help</b>\n\n<b>Main commands:</b>\n/start - Main menu\n/mydocs - My documents\n/stats - Statistics\n/settings - Settings\n/help - This help\n\n<b>How to use:</b>\n1️⃣ Upload a document (PDF, Excel, Word)\n2️⃣ Ask questions about the document\n3️⃣ Use Developer Tools\n4️⃣ Chat with AI without documents\n\n💡 Use the buttons at the bottom for quick access!',
        'de': '❓ <b>Hilfe</b>\n\n<b>Hauptbefehle:</b>\n/start - Hauptmenü\n/mydocs - Meine Dokumente\n/stats - Statistiken\n/settings - Einstellungen\n/help - Diese Hilfe\n\n<b>Wie zu verwenden:</b>\n1️⃣ Laden Sie ein Dokument hoch (PDF, Excel, Word)\n2️⃣ Stellen Sie Fragen zum Dokument\n3️⃣ Verwenden Sie Entwickler-Tools\n4️⃣ Chatten Sie mit KI ohne Dokumente\n\n💡 Verwenden Sie die Schaltflächen unten für schnellen Zugriff!',
    },

    # Errors
    'error_occurred': {
        'ru': '⚠️ Произошла ошибка при обработке вашего запроса.\n\nПожалуйста, попробуйте еще раз.',
        'en': '⚠️ An error occurred while processing your request.\n\nPlease try again.',
        'de': '⚠️ Bei der Verarbeitung Ihrer Anfrage ist ein Fehler aufgetreten.\n\nBitte versuchen Sie es erneut.',
    },
    'feature_in_dev': {
        'ru': '⚙️ Функция в разработке',
        'en': '⚙️ Feature in development',
        'de': '⚙️ Funktion in Entwicklung',
    },

    # Success messages
    'success': {
        'ru': '✅ Успешно!',
        'en': '✅ Success!',
        'de': '✅ Erfolgreich!',
    },
}

def get_text(key: str, lang: str = 'ru', **kwargs) -> str:
    """
    Получает переведенный текст для указанного ключа и языка.

    Args:
        key: Ключ текста
        lang: Код языка (ru, en, de)
        **kwargs: Параметры для форматирования строки

    Returns:
        Переведенный и отформатированный текст
    """
    # Проверяем валидность языка
    if lang not in LANGUAGES:
        lang = 'ru'

    # Получаем текст
    text_dict = TRANSLATIONS.get(key, {})
    text = text_dict.get(lang, text_dict.get('ru', f'[{key}]'))

    # Форматируем если есть параметры
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass

    return text

def get_language_name(lang_code: str) -> str:
    """Возвращает название языка с флагом"""
    return LANGUAGES.get(lang_code, LANGUAGES['ru'])

def get_available_languages() -> dict:
    """Возвращает список доступных языков"""
    return LANGUAGES.copy()
