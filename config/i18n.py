"""
Internationalization (i18n) module for multi-language support.
Supported languages: Russian (ru), English (en), German (de)
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

    # Developer Tools - Detailed messages
    'dev_tools_title': {
        'ru': '💻 <b>Developer Tools</b>\n\nНабор инструментов для разработчиков:\n\n🛠️ <b>Утилиты</b> - JSON, Base64, Hash, UUID, Regex, Cron\n💻 <b>Форматтеры</b> - форматирование кода и данных\n🔐 <b>Генераторы</b> - генерация UUID, паролей, хешей\n🔌 <b>Интеграции</b> - GitHub, NPM, Crypto, Weather\n\n💡 Все инструменты бесплатные и не требуют API ключей!',
        'en': '💻 <b>Developer Tools</b>\n\nDeveloper toolkit:\n\n🛠️ <b>Utilities</b> - JSON, Base64, Hash, UUID, Regex, Cron\n💻 <b>Formatters</b> - code and data formatting\n🔐 <b>Generators</b> - UUID, password, hash generation\n🔌 <b>Integrations</b> - GitHub, NPM, Crypto, Weather\n\n💡 All tools are free and require no API keys!',
        'de': '💻 <b>Entwickler-Tools</b>\n\nEntwickler-Toolkit:\n\n🛠️ <b>Dienstprogramme</b> - JSON, Base64, Hash, UUID, Regex, Cron\n💻 <b>Formatierer</b> - Code- und Datenformatierung\n🔐 <b>Generatoren</b> - UUID-, Passwort-, Hash-Generierung\n🔌 <b>Integrationen</b> - GitHub, NPM, Crypto, Weather\n\n💡 Alle Tools sind kostenlos und benötigen keine API-Schlüssel!',
    },
    'dev_utilities_menu': {
        'ru': '🛠️ <b>Утилиты для разработчиков</b>\n\nВыберите инструмент:\n\n📊 <b>JSON</b> - валидация, форматирование, минификация\n🔣 <b>Base64</b> - кодирование/декодирование\n🔐 <b>Hash</b> - MD5, SHA1, SHA256, SHA512\n🆔 <b>UUID</b> - генерация UUID v4\n🔍 <b>Regex</b> - тестирование регулярных выражений\n🕐 <b>Cron</b> - парсинг cron выражений\n🔢 <b>Калькулятор</b> - с HEX/Binary\n🎨 <b>Цвета</b> - конвертация HEX ↔ RGB\n\n💡 Просто отправьте данные после выбора инструмента',
        'en': '🛠️ <b>Developer Utilities</b>\n\nSelect a tool:\n\n📊 <b>JSON</b> - validation, formatting, minification\n🔣 <b>Base64</b> - encoding/decoding\n🔐 <b>Hash</b> - MD5, SHA1, SHA256, SHA512\n🆔 <b>UUID</b> - UUID v4 generation\n🔍 <b>Regex</b> - regular expression testing\n🕐 <b>Cron</b> - cron expression parsing\n🔢 <b>Calculator</b> - with HEX/Binary\n🎨 <b>Colors</b> - HEX ↔ RGB conversion\n\n💡 Just send data after selecting a tool',
        'de': '🛠️ <b>Entwickler-Dienstprogramme</b>\n\nWählen Sie ein Tool:\n\n📊 <b>JSON</b> - Validierung, Formatierung, Minifizierung\n🔣 <b>Base64</b> - Kodierung/Dekodierung\n🔐 <b>Hash</b> - MD5, SHA1, SHA256, SHA512\n🆔 <b>UUID</b> - UUID v4-Generierung\n🔍 <b>Regex</b> - Reguläre Ausdrücke testen\n🕐 <b>Cron</b> - Cron-Ausdrücke parsen\n🔢 <b>Rechner</b> - mit HEX/Binary\n🎨 <b>Farben</b> - HEX ↔ RGB Konvertierung\n\n💡 Senden Sie einfach Daten nach Auswahl eines Tools',
    },
    'json_tools_menu': {
        'ru': '📊 <b>JSON Инструменты</b>\n\nДоступные действия:\n✅ <b>Validate</b> - проверить корректность JSON\n📝 <b>Format</b> - красиво отформатировать\n🗜️ <b>Minify</b> - сжать в одну строку\n\n💡 Выберите действие, затем отправьте JSON в чат',
        'en': '📊 <b>JSON Tools</b>\n\nAvailable actions:\n✅ <b>Validate</b> - check JSON correctness\n📝 <b>Format</b> - beautify formatting\n🗜️ <b>Minify</b> - compress to one line\n\n💡 Select action, then send JSON to chat',
        'de': '📊 <b>JSON-Tools</b>\n\nVerfügbare Aktionen:\n✅ <b>Validate</b> - JSON-Korrektheit prüfen\n📝 <b>Format</b> - Schön formatieren\n🗜️ <b>Minify</b> - In eine Zeile komprimieren\n\n💡 Aktion wählen, dann JSON in Chat senden',
    },
    'awaiting_json_validate': {
        'ru': '✅ Валидация JSON\n\n📤 Отправьте JSON для проверки\n\n<i>Пример:</i>\n<code>{"name": "John", "age": 30}</code>\n\n⏳ Ожидаю ваш JSON...',
        'en': '✅ JSON Validation\n\n📤 Send JSON for validation\n\n<i>Example:</i>\n<code>{"name": "John", "age": 30}</code>\n\n⏳ Awaiting your JSON...',
        'de': '✅ JSON-Validierung\n\n📤 Senden Sie JSON zur Validierung\n\n<i>Beispiel:</i>\n<code>{"name": "John", "age": 30}</code>\n\n⏳ Warte auf Ihr JSON...',
    },
    'awaiting_json_format': {
        'ru': '📝 Форматирование JSON\n\n📤 Отправьте JSON для форматирования\n\n<i>Пример:</i>\n<code>{"name":"John","age":30}</code>\n\n⏳ Ожидаю ваш JSON...',
        'en': '📝 JSON Formatting\n\n📤 Send JSON for formatting\n\n<i>Example:</i>\n<code>{"name":"John","age":30}</code>\n\n⏳ Awaiting your JSON...',
        'de': '📝 JSON-Formatierung\n\n📤 Senden Sie JSON zur Formatierung\n\n<i>Beispiel:</i>\n<code>{"name":"John","age":30}</code>\n\n⏳ Warte auf Ihr JSON...',
    },
    'awaiting_json_minify': {
        'ru': '🗜️ Минификация JSON\n\n📤 Отправьте JSON для сжатия\n\n<i>Пример:</i>\n<code>{\n  "name": "John",\n  "age": 30\n}</code>\n\n⏳ Ожидаю ваш JSON...',
        'en': '🗜️ JSON Minification\n\n📤 Send JSON for compression\n\n<i>Example:</i>\n<code>{\n  "name": "John",\n  "age": 30\n}</code>\n\n⏳ Awaiting your JSON...',
        'de': '🗜️ JSON-Minifikation\n\n📤 Senden Sie JSON zur Komprimierung\n\n<i>Beispiel:</i>\n<code>{\n  "name": "John",\n  "age": 30\n}</code>\n\n⏳ Warte auf Ihr JSON...',
    },
    'awaiting_base64_encode': {
        'ru': '🔣 <b>Base64 Encoding</b>\n\n📤 Отправьте текст для кодирования\n\n<i>Пример:</i>\n<code>Hello World</code>\n\n⏳ Ожидаю текст...',
        'en': '🔣 <b>Base64 Encoding</b>\n\n📤 Send text for encoding\n\n<i>Example:</i>\n<code>Hello World</code>\n\n⏳ Awaiting text...',
        'de': '🔣 <b>Base64-Kodierung</b>\n\n📤 Senden Sie Text zur Kodierung\n\n<i>Beispiel:</i>\n<code>Hallo Welt</code>\n\n⏳ Warte auf Text...',
    },
    'awaiting_base64_decode': {
        'ru': '🔓 <b>Base64 Decoding</b>\n\n📤 Отправьте Base64 строку для декодирования\n\n<i>Пример:</i>\n<code>SGVsbG8gV29ybGQ=</code>\n\n⏳ Ожидаю Base64...',
        'en': '🔓 <b>Base64 Decoding</b>\n\n📤 Send Base64 string for decoding\n\n<i>Example:</i>\n<code>SGVsbG8gV29ybGQ=</code>\n\n⏳ Awaiting Base64...',
        'de': '🔓 <b>Base64-Dekodierung</b>\n\n📤 Senden Sie Base64-String zur Dekodierung\n\n<i>Beispiel:</i>\n<code>SGVsbG8gV29ybGQ=</code>\n\n⏳ Warte auf Base64...',
    },
    'hash_menu': {
        'ru': '🔐 <b>Hash Generator</b>\n\nВыберите алгоритм хеширования:\n\n• <b>MD5</b> - 128 bit (не рекомендуется для безопасности)\n• <b>SHA1</b> - 160 bit\n• <b>SHA256</b> - 256 bit (рекомендуется)\n• <b>SHA512</b> - 512 bit (максимальная безопасность)\n\n💡 После выбора отправьте текст для хеширования',
        'en': '🔐 <b>Hash Generator</b>\n\nSelect hashing algorithm:\n\n• <b>MD5</b> - 128 bit (not recommended for security)\n• <b>SHA1</b> - 160 bit\n• <b>SHA256</b> - 256 bit (recommended)\n• <b>SHA512</b> - 512 bit (maximum security)\n\n💡 After selection, send text for hashing',
        'de': '🔐 <b>Hash-Generator</b>\n\nWählen Sie Hash-Algorithmus:\n\n• <b>MD5</b> - 128 bit (nicht empfohlen für Sicherheit)\n• <b>SHA1</b> - 160 bit\n• <b>SHA256</b> - 256 bit (empfohlen)\n• <b>SHA512</b> - 512 bit (maximale Sicherheit)\n\n💡 Nach Auswahl Text zum Hashen senden',
    },
    'awaiting_hash': {
        'ru': '🔐 <b>Hash Generator - {algorithm}</b>\n\n📤 Отправьте текст для хеширования\n\n<i>Примеры:</i>\n<code>password123</code>\n<code>mySecretKey</code>\n\n⏳ Ожидаю текст...',
        'en': '🔐 <b>Hash Generator - {algorithm}</b>\n\n📤 Send text for hashing\n\n<i>Examples:</i>\n<code>password123</code>\n<code>mySecretKey</code>\n\n⏳ Awaiting text...',
        'de': '🔐 <b>Hash-Generator - {algorithm}</b>\n\n📤 Senden Sie Text zum Hashen\n\n<i>Beispiele:</i>\n<code>passwort123</code>\n<code>meinGeheimSchlüssel</code>\n\n⏳ Warte auf Text...',
    },
    'integrations_menu': {
        'ru': '🔌 <b>Бесплатные API интеграции</b>\n\nДоступные сервисы:\n\n🐙 <b>GitHub</b> - поиск репозиториев\n📦 <b>NPM</b> - информация о пакетах\n👤 <b>GitHub User</b> - профили пользователей\n🌐 <b>Can I Use</b> - поддержка веб-фичей\n💰 <b>Crypto Price</b> - цены криптовалют\n🌤️ <b>Weather</b> - погода в городах\n💭 <b>Quote</b> - мотивационные цитаты\n😄 <b>Joke</b> - шутки для программистов\n\n💡 Все API бесплатные, без ключей!',
        'en': '🔌 <b>Free API Integrations</b>\n\nAvailable services:\n\n🐙 <b>GitHub</b> - repository search\n📦 <b>NPM</b> - package information\n👤 <b>GitHub User</b> - user profiles\n🌐 <b>Can I Use</b> - web feature support\n💰 <b>Crypto Price</b> - cryptocurrency prices\n🌤️ <b>Weather</b> - city weather\n💭 <b>Quote</b> - motivational quotes\n😄 <b>Joke</b> - programmer jokes\n\n💡 All APIs are free, no keys needed!',
        'de': '🔌 <b>Kostenlose API-Integrationen</b>\n\nVerfügbare Dienste:\n\n🐙 <b>GitHub</b> - Repository-Suche\n📦 <b>NPM</b> - Paketinformationen\n👤 <b>GitHub User</b> - Benutzerprofile\n🌐 <b>Can I Use</b> - Web-Feature-Unterstützung\n💰 <b>Crypto Price</b> - Kryptowährungspreise\n🌤️ <b>Weather</b> - Stadtwetter\n💭 <b>Quote</b> - Motivationszitate\n😄 <b>Joke</b> - Programmierer-Witze\n\n💡 Alle APIs sind kostenlos, keine Schlüssel erforderlich!',
    },
    'upload_instruction': {
        'ru': '📤 <b>Загрузка документа</b>\n\nОтправьте мне файл одного из форматов:\n• 📄 PDF\n• 📊 Excel (.xlsx, .xls)\n• 📝 Word (.docx)\n• 🎤 Аудио (для транскрипции)\n• 🌐 URL (ссылка на веб-страницу)\n\nЯ обработаю его и вы сможете задавать вопросы по содержимому!',
        'en': '📤 <b>Upload Document</b>\n\nSend me a file in one of these formats:\n• 📄 PDF\n• 📊 Excel (.xlsx, .xls)\n• 📝 Word (.docx)\n• 🎤 Audio (for transcription)\n• 🌐 URL (web page link)\n\nI\'ll process it and you can ask questions about the content!',
        'de': '📤 <b>Dokument hochladen</b>\n\nSenden Sie mir eine Datei in einem dieser Formate:\n• 📄 PDF\n• 📊 Excel (.xlsx, .xls)\n• 📝 Word (.docx)\n• 🎤 Audio (zur Transkription)\n• 🌐 URL (Webseiten-Link)\n\nIch verarbeite es und Sie können Fragen zum Inhalt stellen!',
    },
}

def get_text(key: str, lang: str = 'ru', **kwargs) -> str:
    """
    Get translated text for specified key and language.

    Args:
        key: Text key
        lang: Language code (ru, en, de)
        **kwargs: Parameters for string formatting

    Returns:
        Translated and formatted text
    """
    # Validate language
    if lang not in LANGUAGES:
        lang = 'ru'

    # Get text
    text_dict = TRANSLATIONS.get(key, {})
    text = text_dict.get(lang, text_dict.get('ru', f'[{key}]'))

    # Format if parameters provided
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass

    return text

def get_language_name(lang_code: str) -> str:
    """Returns language name with flag"""
    return LANGUAGES.get(lang_code, LANGUAGES['ru'])

def get_available_languages() -> dict:
    """Returns list of available languages"""
    return LANGUAGES.copy()
