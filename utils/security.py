"""
Security utilities for file validation, input sanitization, and security checks.
"""
import os
import re
from typing import Optional, Tuple
from pathlib import Path
import logging

# Пытаемся импортировать python-magic, но не падаем если его нет
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    logging.warning(
        "python-magic not available. MIME type validation will be skipped. "
        "Install python-magic-bin on Windows: pip install python-magic-bin"
    )


# Максимальные размеры файлов (в байтах)
MAX_FILE_SIZES = {
    'pdf': 50 * 1024 * 1024,      # 50 MB
    'excel': 20 * 1024 * 1024,    # 20 MB
    'word': 20 * 1024 * 1024,     # 20 MB
    'audio': 25 * 1024 * 1024,    # 25 MB
}

# Разрешенные MIME types
ALLOWED_MIME_TYPES = {
    'pdf': ['application/pdf'],
    'excel': [
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # .xlsx
        'application/vnd.ms-excel',  # .xls
    ],
    'word': [
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
        'application/msword',  # .doc
    ],
    'audio': [
        'audio/mpeg',      # .mp3
        'audio/wav',       # .wav
        'audio/ogg',       # .ogg
        'audio/x-m4a',     # .m4a
        'audio/mp4',       # .m4a альтернативный MIME
    ],
}

# Разрешенные расширения
ALLOWED_EXTENSIONS = {
    'pdf': ['.pdf'],
    'excel': ['.xlsx', '.xls'],
    'word': ['.docx', '.doc'],
    'audio': ['.mp3', '.wav', '.ogg', '.m4a'],
}


class FileValidationError(Exception):
    """Исключение при ошибке валидации файла."""
    pass


class SecurityError(Exception):
    """Исключение при обнаружении угрозы безопасности."""
    pass


def validate_file_extension(filename: str, file_type: str) -> bool:
    """
    Проверка расширения файла.

    Args:
        filename: Имя файла
        file_type: Тип файла ('pdf', 'excel', 'word', 'audio')

    Returns:
        True если расширение разрешено

    Raises:
        FileValidationError: Если расширение не разрешено
    """
    ext = Path(filename).suffix.lower()

    if file_type not in ALLOWED_EXTENSIONS:
        raise FileValidationError(f"Unknown file type: {file_type}")

    if ext not in ALLOWED_EXTENSIONS[file_type]:
        allowed = ', '.join(ALLOWED_EXTENSIONS[file_type])
        raise FileValidationError(
            f"File extension '{ext}' not allowed for {file_type}. "
            f"Allowed: {allowed}"
        )

    return True


def validate_file_size(file_path: str, file_type: str) -> bool:
    """
    Проверка размера файла.

    Args:
        file_path: Путь к файлу
        file_type: Тип файла ('pdf', 'excel', 'word', 'audio')

    Returns:
        True если размер допустимый

    Raises:
        FileValidationError: Если файл слишком большой
    """
    if not os.path.exists(file_path):
        raise FileValidationError(f"File not found: {file_path}")

    file_size = os.path.getsize(file_path)
    max_size = MAX_FILE_SIZES.get(file_type, 10 * 1024 * 1024)  # Default 10 MB

    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        current_mb = file_size / (1024 * 1024)
        raise FileValidationError(
            f"File too large: {current_mb:.2f} MB. Maximum allowed: {max_mb:.2f} MB"
        )

    if file_size == 0:
        raise FileValidationError("File is empty (0 bytes)")

    return True


def validate_mime_type(file_path: str, file_type: str) -> bool:
    """
    Проверка MIME type файла через magic bytes.

    Args:
        file_path: Путь к файлу
        file_type: Ожидаемый тип файла

    Returns:
        True если MIME type соответствует

    Raises:
        FileValidationError: Если MIME type не соответствует
    """
    # Если python-magic недоступен, пропускаем MIME проверку
    if not MAGIC_AVAILABLE:
        logging.debug(f"Skipping MIME type check for {file_path} (magic not available)")
        return True

    try:
        mime = magic.Magic(mime=True)
        detected_mime = mime.from_file(file_path)
    except Exception as e:
        # Если ошибка при проверке, логируем и пропускаем
        logging.warning(f"Could not check MIME type for {file_path}: {e}")
        return True

    allowed_mimes = ALLOWED_MIME_TYPES.get(file_type, [])

    if detected_mime not in allowed_mimes:
        raise FileValidationError(
            f"Invalid file type. Detected MIME: {detected_mime}. "
            f"Expected one of: {', '.join(allowed_mimes)}"
        )

    return True


def sanitize_filename(filename: str) -> str:
    """
    Санитизация имени файла - удаление опасных символов.

    Args:
        filename: Исходное имя файла

    Returns:
        Безопасное имя файла
    """
    # Удаляем path traversal атаки
    filename = os.path.basename(filename)

    # Удаляем опасные символы, оставляем только буквы, цифры, точки, дефисы, подчеркивания
    filename = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)

    # Ограничиваем длину
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255 - len(ext)] + ext

    return filename


def sanitize_text_input(text: str, max_length: int = 10000) -> str:
    """
    Санитизация текстового ввода пользователя.

    Args:
        text: Входной текст
        max_length: Максимальная длина

    Returns:
        Очищенный текст

    Raises:
        SecurityError: Если обнаружены опасные паттерны
    """
    # Ограничиваем длину
    if len(text) > max_length:
        text = text[:max_length]

    # Проверяем на SQL injection паттерны (базовая проверка)
    sql_patterns = [
        r"(\bUNION\b.*\bSELECT\b)",
        r"(\bDROP\b.*\bTABLE\b)",
        r"(\bINSERT\b.*\bINTO\b)",
        r"(\bDELETE\b.*\bFROM\b)",
        r"(;\s*DROP\b)",
        r"(--)",  # SQL comment marker
        r"(/\*.*\*/)",
        r"('.*OR.*'.*=.*')",  # OR-based injection like 1' OR '1'='1
    ]

    for pattern in sql_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            raise SecurityError(f"Potentially dangerous SQL pattern detected")

    # Проверяем на command injection
    command_patterns = [
        r"(&&|\|\||;|\$\(|\`)",
        r"(>\s*/dev/)",
        r"(<\s*/dev/)",
    ]

    for pattern in command_patterns:
        if re.search(pattern, text):
            raise SecurityError(f"Potentially dangerous command injection pattern detected")

    return text


def validate_url(url: str) -> Tuple[bool, str]:
    """
    Валидация URL перед скрапингом.

    Args:
        url: URL для проверки

    Returns:
        (is_valid, error_message)
    """
    # Блокируем опасные схемы (проверяем первым делом)
    if url.startswith(('file://', 'ftp://', 'data:')):
        return False, "URL scheme not allowed"

    # Базовая проверка формата
    url_pattern = re.compile(
        r'^https?://'  # http:// или https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...или IP
        r'(?::\d+)?'  # опциональный порт
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )

    if not url_pattern.match(url):
        return False, "Invalid URL format"

    # Блокируем localhost и internal IPs для production
    localhost_patterns = [
        'localhost',
        '127.0.0.1',
        '0.0.0.0',
        '192.168.',
        '10.',
        '172.16.',
        '172.17.',
        '172.18.',
        '172.19.',
        '172.20.',
        '172.21.',
        '172.22.',
        '172.23.',
        '172.24.',
        '172.25.',
        '172.26.',
        '172.27.',
        '172.28.',
        '172.29.',
        '172.30.',
        '172.31.',
    ]

    for pattern in localhost_patterns:
        if pattern in url.lower():
            return False, "Access to internal/localhost URLs not allowed"

    # Ограничиваем длину URL
    if len(url) > 2000:
        return False, "URL too long (max 2000 characters)"

    return True, ""


def validate_file(file_path: str, filename: str, file_type: str) -> Tuple[bool, str]:
    """
    Комплексная валидация файла.

    Args:
        file_path: Путь к файлу
        filename: Оригинальное имя файла
        file_type: Тип файла ('pdf', 'excel', 'word', 'audio')

    Returns:
        (is_valid, error_message)
    """
    try:
        # 1. Проверка расширения
        validate_file_extension(filename, file_type)

        # 2. Проверка размера
        validate_file_size(file_path, file_type)

        # 3. Проверка MIME type
        validate_mime_type(file_path, file_type)

        return True, ""

    except FileValidationError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def get_safe_file_path(base_dir: str, user_id: int, filename: str) -> str:
    """
    Генерация безопасного пути для сохранения файла.

    Args:
        base_dir: Базовая директория
        user_id: ID пользователя
        filename: Имя файла

    Returns:
        Безопасный путь к файлу
    """
    # Санитизация имени файла
    safe_filename = sanitize_filename(filename)

    # Создаем уникальное имя с timestamp (включая микросекунды для уникальности)
    import time
    timestamp = time.time()  # Включает микросекунды
    timestamp_str = f"{int(timestamp)}_{int((timestamp % 1) * 1000000)}"
    name, ext = os.path.splitext(safe_filename)
    unique_filename = f"{user_id}_{timestamp_str}_{name}{ext}"

    # Создаем путь
    user_dir = os.path.join(base_dir, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    return os.path.join(user_dir, unique_filename)


# Пример использования
if __name__ == "__main__":
    # Тест валидации файла
    print("Testing file validation...")

    # Тест санитизации
    print("\nTesting filename sanitization...")
    dangerous_names = [
        "../../etc/passwd",
        "file<script>alert(1)</script>.pdf",
        "test\x00file.pdf",
        "очень_длинное_имя_файла" * 50 + ".pdf",
    ]

    for name in dangerous_names:
        safe = sanitize_filename(name)
        print(f"Original: {name[:50]}... -> Safe: {safe}")

    # Тест URL валидации
    print("\nTesting URL validation...")
    test_urls = [
        "https://example.com",
        "http://localhost:8000",
        "file:///etc/passwd",
        "https://192.168.1.1",
    ]

    for url in test_urls:
        is_valid, msg = validate_url(url)
        status = "✅" if is_valid else "❌"
        print(f"{status} {url}: {msg if msg else 'OK'}")
