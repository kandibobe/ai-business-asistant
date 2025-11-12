"""
Инструменты для разработчиков - утилиты и форматтеры.
Бесплатные инструменты без внешних API.
"""
import json
import re
import base64
import hashlib
import uuid
from typing import Dict, Any, Tuple


def format_json(text: str, indent: int = 2) -> Tuple[bool, str]:
    """
    Форматирует JSON с отступами.

    Returns:
        (success, result) - успех и отформатированный JSON или ошибка
    """
    try:
        data = json.loads(text)
        formatted = json.dumps(data, indent=indent, ensure_ascii=False, sort_keys=True)
        return True, f"```json\n{formatted}\n```"
    except json.JSONDecodeError as e:
        return False, f"❌ Ошибка JSON: {str(e)}"


def minify_json(text: str) -> Tuple[bool, str]:
    """Минифицирует JSON (убирает пробелы)"""
    try:
        data = json.loads(text)
        minified = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
        return True, f"```\n{minified}\n```"
    except json.JSONDecodeError as e:
        return False, f"❌ Ошибка JSON: {str(e)}"


def validate_json(text: str) -> Tuple[bool, str]:
    """Валидирует JSON"""
    try:
        data = json.loads(text)
        keys_count = len(data) if isinstance(data, dict) else len(data) if isinstance(data, list) else 0

        result = "✅ <b>JSON валиден!</b>\n\n"
        result += f"📊 Тип: {type(data).__name__}\n"

        if isinstance(data, dict):
            result += f"🔑 Ключей: {len(data)}\n"
            result += f"📝 Ключи: {', '.join(list(data.keys())[:10])}"
            if len(data) > 10:
                result += "..."
        elif isinstance(data, list):
            result += f"📋 Элементов: {len(data)}\n"

        return True, result
    except json.JSONDecodeError as e:
        return False, f"❌ <b>JSON невалиден</b>\n\nОшибка: {str(e)}"


def encode_base64(text: str) -> str:
    """Кодирует текст в Base64"""
    encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
    return f"```\n{encoded}\n```"


def decode_base64(text: str) -> Tuple[bool, str]:
    """Декодирует Base64"""
    try:
        decoded = base64.b64decode(text).decode('utf-8')
        return True, f"```\n{decoded}\n```"
    except Exception as e:
        return False, f"❌ Ошибка декодирования: {str(e)}"


def generate_hash(text: str, algorithm: str = 'sha256') -> str:
    """
    Генерирует хеш для текста.

    Args:
        text: Текст для хеширования
        algorithm: Алгоритм (md5, sha1, sha256, sha512)
    """
    text_bytes = text.encode('utf-8')

    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
    }

    hash_func = algorithms.get(algorithm.lower(), hashlib.sha256)
    hash_result = hash_func(text_bytes).hexdigest()

    result = f"<b>Hash ({algorithm.upper()}):</b>\n\n"
    result += f"<code>{hash_result}</code>\n\n"
    result += f"📏 Длина: {len(hash_result)} символов"

    return result


def generate_uuids(count: int = 5) -> str:
    """Генерирует UUID"""
    result = f"<b>UUID v4 ({count} штук):</b>\n\n"

    for i in range(min(count, 10)):  # Максимум 10
        uid = str(uuid.uuid4())
        result += f"<code>{uid}</code>\n"

    return result


def parse_regex(pattern: str, text: str, flags: str = '') -> Tuple[bool, str]:
    """
    Тестирует регулярное выражение.

    Args:
        pattern: Regex паттерн
        text: Текст для поиска
        flags: Флаги (i - ignorecase, m - multiline, s - dotall)
    """
    try:
        # Преобразуем флаги
        re_flags = 0
        if 'i' in flags.lower():
            re_flags |= re.IGNORECASE
        if 'm' in flags.lower():
            re_flags |= re.MULTILINE
        if 's' in flags.lower():
            re_flags |= re.DOTALL

        matches = re.findall(pattern, text, re_flags)

        if matches:
            result = f"✅ <b>Найдено совпадений: {len(matches)}</b>\n\n"
            result += "<b>Результаты:</b>\n"

            for i, match in enumerate(matches[:10], 1):  # Показываем первые 10
                if isinstance(match, tuple):
                    match_str = ' | '.join(str(m) for m in match)
                else:
                    match_str = str(match)
                result += f"{i}. <code>{match_str}</code>\n"

            if len(matches) > 10:
                result += f"\n<i>... и еще {len(matches) - 10} совпадений</i>"

            return True, result
        else:
            return False, "❌ Совпадений не найдено"

    except re.error as e:
        return False, f"❌ Ошибка в regex: {str(e)}"


def format_sql(sql: str) -> str:
    """Базовое форматирование SQL (простое)"""
    # Простой форматтер SQL
    keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT JOIN', 'RIGHT JOIN',
                'INNER JOIN', 'ON', 'GROUP BY', 'ORDER BY', 'HAVING',
                'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP']

    formatted = sql
    for keyword in keywords:
        # Добавляем переносы строк перед ключевыми словами
        formatted = re.sub(f'\\b{keyword}\\b', f'\n{keyword}', formatted, flags=re.IGNORECASE)

    # Убираем лишние пробелы
    formatted = '\n'.join(line.strip() for line in formatted.split('\n') if line.strip())

    return f"```sql\n{formatted}\n```"


def parse_cron(expression: str) -> Tuple[bool, str]:
    """Парсит и объясняет cron выражение"""
    try:
        parts = expression.split()
        if len(parts) != 5:
            return False, "❌ Cron должен состоять из 5 частей: минута час день месяц день_недели"

        minute, hour, day, month, weekday = parts

        result = "🕐 <b>Cron Expression</b>\n\n"
        result += f"<code>{expression}</code>\n\n"
        result += "<b>Расшифровка:</b>\n"
        result += f"⏰ Минута: {minute}\n"
        result += f"🕐 Час: {hour}\n"
        result += f"📅 День месяца: {day}\n"
        result += f"📆 Месяц: {month}\n"
        result += f"📌 День недели: {weekday}\n\n"

        # Простое объяснение
        if expression == "* * * * *":
            result += "💡 <i>Каждую минуту</i>"
        elif expression == "0 * * * *":
            result += "💡 <i>Каждый час</i>"
        elif expression == "0 0 * * *":
            result += "💡 <i>Каждый день в полночь</i>"
        elif expression == "0 0 * * 0":
            result += "💡 <i>Каждое воскресенье в полночь</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Ошибка парсинга: {str(e)}"


def calculate_expression(expr: str) -> Tuple[bool, str]:
    """
    Безопасный калькулятор для математических выражений.

    SECURITY FIX: Replaces unsafe eval() with AST-based evaluation.
    Only allows whitelisted mathematical operations to prevent code injection.
    """
    import ast
    import operator

    # Whitelist of allowed operations
    ALLOWED_OPS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def safe_eval(node):
        """Recursively evaluate AST node with whitelist of operations."""
        if isinstance(node, ast.Num):  # Number (Python < 3.8)
            return node.n
        elif isinstance(node, ast.Constant):  # Constant (Python 3.8+)
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numeric constants allowed")
        elif isinstance(node, ast.BinOp):  # Binary operation (+, -, *, /, etc.)
            op_type = type(node.op)
            if op_type not in ALLOWED_OPS:
                raise ValueError(f"Operation {op_type.__name__} not allowed")
            left = safe_eval(node.left)
            right = safe_eval(node.right)
            return ALLOWED_OPS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):  # Unary operation (-, +)
            op_type = type(node.op)
            if op_type not in ALLOWED_OPS:
                raise ValueError(f"Operation {op_type.__name__} not allowed")
            operand = safe_eval(node.operand)
            return ALLOWED_OPS[op_type](operand)
        else:
            raise ValueError(f"Unsupported operation: {type(node).__name__}")

    try:
        # Parse expression into AST
        tree = ast.parse(expr, mode='eval')

        # Evaluate safely (no eval() vulnerability)
        result = safe_eval(tree.body)

        output = f"🔢 <b>Результат:</b>\n\n"
        output += f"<code>{expr} = {result}</code>\n\n"

        # Дополнительные форматы
        if isinstance(result, (int, float)):
            output += "<b>Форматы:</b>\n"
            output += f"💯 Десятичное: {result}\n"
            if isinstance(result, float):
                output += f"🔢 Целое: {int(result)}\n"
            if result >= 0 and abs(result) < 2**63:  # Prevent overflow
                try:
                    output += f"🔣 Hex: {hex(int(result))}\n"
                    output += f"2️⃣ Binary: {bin(int(result))}\n"
                except (ValueError, OverflowError):
                    pass  # Skip if number too large

        return True, output

    except SyntaxError:
        return False, "❌ Синтаксическая ошибка в выражении"
    except ZeroDivisionError:
        return False, "❌ Деление на ноль"
    except ValueError as e:
        return False, f"❌ Недопустимая операция: {str(e)}"
    except OverflowError:
        return False, "❌ Результат слишком большой"
    except Exception as e:
        return False, f"❌ Ошибка вычисления: {str(e)}"


def color_converter(color: str) -> Tuple[bool, str]:
    """Конвертирует цвета между форматами (HEX, RGB)"""
    color = color.strip()

    # HEX to RGB
    if color.startswith('#'):
        try:
            hex_color = color.lstrip('#')
            if len(hex_color) == 6:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)

                result = f"🎨 <b>Конвертация цвета</b>\n\n"
                result += f"🔤 HEX: <code>{color}</code>\n"
                result += f"🎨 RGB: <code>rgb({r}, {g}, {b})</code>\n"
                result += f"📊 RGB %: <code>rgb({r/255*100:.1f}%, {g/255*100:.1f}%, {b/255*100:.1f}%)</code>\n"

                return True, result
            else:
                return False, "❌ HEX должен быть в формате #RRGGBB"
        except ValueError:
            return False, "❌ Некорректный HEX цвет"

    # RGB to HEX
    rgb_match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color)
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        if all(0 <= c <= 255 for c in [r, g, b]):
            hex_color = f"#{r:02x}{g:02x}{b:02x}"

            result = f"🎨 <b>Конвертация цвета</b>\n\n"
            result += f"🎨 RGB: <code>rgb({r}, {g}, {b})</code>\n"
            result += f"🔤 HEX: <code>{hex_color}</code>\n"
            result += f"🔤 HEX (upper): <code>{hex_color.upper()}</code>\n"

            return True, result
        else:
            return False, "❌ RGB значения должны быть 0-255"

    return False, "❌ Формат не распознан. Используйте #RRGGBB или rgb(r, g, b)"


def generate_password(length: int = 16, include_special: bool = True) -> str:
    """Генерирует случайный пароль"""
    import random
    import string

    chars = string.ascii_letters + string.digits
    if include_special:
        chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"

    password = ''.join(random.choice(chars) for _ in range(length))

    result = f"🔐 <b>Сгенерированный пароль:</b>\n\n"
    result += f"<code>{password}</code>\n\n"
    result += f"📏 Длина: {length} символов\n"
    result += f"🔤 Специальные символы: {'✅ Да' if include_special else '❌ Нет'}"

    return result


def url_encode(text: str) -> str:
    """URL encoding"""
    from urllib.parse import quote
    encoded = quote(text)
    return f"<b>URL Encoded:</b>\n\n<code>{encoded}</code>"


def url_decode(text: str) -> Tuple[bool, str]:
    """URL decoding"""
    from urllib.parse import unquote
    try:
        decoded = unquote(text)
        return True, f"<b>URL Decoded:</b>\n\n<code>{decoded}</code>"
    except Exception as e:
        return False, f"❌ Ошибка декодирования: {str(e)}"


def timestamp_to_date(timestamp: str) -> Tuple[bool, str]:
    """Конвертирует Unix timestamp в дату"""
    from datetime import datetime
    try:
        ts = int(timestamp)

        # Если timestamp в миллисекундах
        if ts > 10000000000:
            ts = ts / 1000

        dt = datetime.fromtimestamp(ts)

        result = f"📅 <b>Конвертация timestamp</b>\n\n"
        result += f"🔢 Timestamp: <code>{timestamp}</code>\n\n"
        result += f"📆 Дата: <code>{dt.strftime('%Y-%m-%d')}</code>\n"
        result += f"🕐 Время: <code>{dt.strftime('%H:%M:%S')}</code>\n"
        result += f"📅 Полный формат: <code>{dt.strftime('%Y-%m-%d %H:%M:%S')}</code>\n"
        result += f"🌍 ISO 8601: <code>{dt.isoformat()}</code>\n"

        return True, result
    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"
