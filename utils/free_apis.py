"""
Бесплатные API интеграции для разработчиков.
Все API не требуют API ключей или имеют щедрые бесплатные лимиты.
"""
import requests
from typing import Dict, Any, List, Tuple
from datetime import datetime


def search_github_repos(query: str, limit: int = 5) -> Tuple[bool, str]:
    """
    Поиск репозиториев на GitHub (без API ключа).

    Args:
        query: Поисковый запрос
        limit: Количество результатов (макс 10)

    Returns:
        (success, result_message)
    """
    try:
        url = "https://api.github.com/search/repositories"
        params = {
            'q': query,
            'sort': 'stars',
            'order': 'desc',
            'per_page': min(limit, 10)
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        repos = data.get('items', [])

        if not repos:
            return False, f"❌ Репозитории по запросу '{query}' не найдены"

        result = f"🔍 <b>GitHub: найдено {data.get('total_count', 0):,} репозиториев</b>\n\n"
        result += f"<b>Топ {len(repos)} результатов:</b>\n\n"

        for i, repo in enumerate(repos, 1):
            name = repo.get('full_name', 'N/A')
            description = repo.get('description', 'Нет описания')[:100]
            stars = repo.get('stargazers_count', 0)
            language = repo.get('language', 'N/A')
            url = repo.get('html_url', '')

            result += f"{i}. <b>{name}</b>\n"
            result += f"   ⭐ {stars:,} | 💻 {language}\n"
            result += f"   📝 {description}\n"
            result += f"   🔗 {url}\n\n"

        return True, result

    except requests.RequestException as e:
        return False, f"❌ Ошибка запроса: {str(e)}"
    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"


def search_npm_package(query: str) -> Tuple[bool, str]:
    """
    Поиск npm пакетов.

    Args:
        query: Название пакета

    Returns:
        (success, result_message)
    """
    try:
        url = f"https://registry.npmjs.org/{query}"
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            return False, f"❌ Пакет '{query}' не найден на NPM"

        response.raise_for_status()
        data = response.json()

        # Получаем последнюю версию
        latest_version = data.get('dist-tags', {}).get('latest', 'N/A')
        description = data.get('description', 'Нет описания')
        homepage = data.get('homepage', 'N/A')
        repo_url = data.get('repository', {})
        if isinstance(repo_url, dict):
            repo_url = repo_url.get('url', 'N/A')

        # Получаем информацию о версии
        versions = data.get('versions', {})
        latest_info = versions.get(latest_version, {})

        result = f"📦 <b>NPM Package: {query}</b>\n\n"
        result += f"🏷️ Последняя версия: <code>{latest_version}</code>\n"
        result += f"📝 Описание: {description}\n\n"

        # Dependencies
        dependencies = latest_info.get('dependencies', {})
        if dependencies:
            result += f"📚 Зависимостей: {len(dependencies)}\n"

        # Keywords
        keywords = data.get('keywords', [])
        if keywords:
            result += f"🏷️ Теги: {', '.join(keywords[:5])}\n"

        result += f"\n🌐 Homepage: {homepage}\n"
        result += f"📂 Repo: {repo_url}\n"
        result += f"📥 Установка: <code>npm install {query}</code>"

        return True, result

    except requests.RequestException as e:
        return False, f"❌ Ошибка запроса: {str(e)}"
    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"


def check_browser_support(feature: str) -> Tuple[bool, str]:
    """
    Проверяет поддержку веб-фичи в браузерах через Can I Use API.

    Args:
        feature: Название фичи (например, 'flexbox', 'css-grid')

    Returns:
        (success, result_message)
    """
    try:
        # Используем публичный API caniuse
        url = f"https://caniuse.com/process/query"
        params = {'search': feature}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        # Альтернативный подход - используем статичные данные
        result = f"🌐 <b>Browser Support: {feature}</b>\n\n"
        result += f"🔍 Проверьте полную информацию:\n"
        result += f"🔗 https://caniuse.com/?search={feature}\n\n"
        result += f"💡 <i>Для детальной информации о поддержке браузерами,\n"
        result += f"посетите Can I Use по ссылке выше</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"


def get_public_ip() -> Tuple[bool, str]:
    """Получает публичный IP адрес"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        data = response.json()
        ip = data.get('ip', 'N/A')

        result = f"🌐 <b>Ваш публичный IP:</b>\n\n"
        result += f"<code>{ip}</code>\n\n"
        result += f"💡 <i>Это IP адрес бота, не пользователя</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"


def get_random_quote() -> Tuple[bool, str]:
    """Получает случайную мотивационную цитату"""
    try:
        response = requests.get('https://api.quotable.io/random', timeout=5)
        response.raise_for_status()
        data = response.json()

        quote = data.get('content', '')
        author = data.get('author', 'Unknown')

        result = f"💭 <b>Цитата дня:</b>\n\n"
        result += f"<i>"{quote}"</i>\n\n"
        result += f"— <b>{author}</b>"

        return True, result

    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"


def get_random_joke() -> Tuple[bool, str]:
    """Получает случайную шутку для программистов"""
    try:
        response = requests.get('https://official-joke-api.appspot.com/random_joke', timeout=5)
        response.raise_for_status()
        data = response.json()

        setup = data.get('setup', '')
        punchline = data.get('punchline', '')

        result = f"😄 <b>Шутка для программистов:</b>\n\n"
        result += f"{setup}\n\n"
        result += f"<i>{punchline}</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"


def get_crypto_price(crypto: str = 'bitcoin') -> Tuple[bool, str]:
    """
    Получает текущую цену криптовалюты.

    Args:
        crypto: Название крипты (bitcoin, ethereum, etc)

    Returns:
        (success, result_message)
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': crypto.lower(),
            'vs_currencies': 'usd,rub',
            'include_24hr_change': 'true'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if crypto.lower() not in data:
            return False, f"❌ Криптовалюта '{crypto}' не найдена"

        crypto_data = data[crypto.lower()]
        price_usd = crypto_data.get('usd', 0)
        price_rub = crypto_data.get('rub', 0)
        change_24h = crypto_data.get('usd_24h_change', 0)

        change_icon = "📈" if change_24h > 0 else "📉"
        change_color = "+" if change_24h > 0 else ""

        result = f"💰 <b>{crypto.capitalize()} Price</b>\n\n"
        result += f"💵 ${price_usd:,.2f}\n"
        result += f"💴 ₽{price_rub:,.2f}\n\n"
        result += f"{change_icon} 24h: {change_color}{change_24h:.2f}%\n\n"
        result += f"<i>Данные от CoinGecko</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"


def generate_qr_code(text: str) -> Tuple[bool, str]:
    """
    Генерирует ссылку на QR код.

    Args:
        text: Текст для QR кода

    Returns:
        (success, url_to_qr_code)
    """
    try:
        from urllib.parse import quote
        encoded_text = quote(text)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_text}"

        result = f"📱 <b>QR Code сгенерирован!</b>\n\n"
        result += f"🔗 URL: {qr_url}\n\n"
        result += f"💡 <i>Откройте ссылку чтобы увидеть QR код</i>"

        return True, qr_url

    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"


def shorten_url(long_url: str) -> Tuple[bool, str]:
    """
    Сокращает URL через бесплатный сервис.

    Args:
        long_url: Длинный URL

    Returns:
        (success, short_url)
    """
    try:
        # Используем is.gd - бесплатный без API ключа
        url = "https://is.gd/create.php"
        params = {
            'format': 'json',
            'url': long_url
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        short_url = data.get('shorturl', '')

        if short_url:
            result = f"🔗 <b>URL сокращен!</b>\n\n"
            result += f"📎 Оригинал: <code>{long_url[:50]}...</code>\n"
            result += f"✂️ Короткий: <code>{short_url}</code>\n\n"
            result += f"💡 <i>Скопируйте короткую ссылку</i>"

            return True, result
        else:
            return False, "❌ Не удалось сократить URL"

    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"


def get_github_user_info(username: str) -> Tuple[bool, str]:
    """
    Получает информацию о пользователе GitHub.

    Args:
        username: GitHub username

    Returns:
        (success, user_info)
    """
    try:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            return False, f"❌ Пользователь '{username}' не найден"

        response.raise_for_status()
        data = response.json()

        name = data.get('name', username)
        bio = data.get('bio', 'Нет био')
        public_repos = data.get('public_repos', 0)
        followers = data.get('followers', 0)
        following = data.get('following', 0)
        location = data.get('location', 'N/A')
        blog = data.get('blog', '')
        twitter = data.get('twitter_username', '')

        result = f"👤 <b>GitHub: {name}</b>\n\n"
        result += f"🆔 Username: <code>{username}</code>\n"
        result += f"📝 Bio: {bio}\n\n"
        result += f"📦 Репозиториев: {public_repos}\n"
        result += f"👥 Followers: {followers}\n"
        result += f"👤 Following: {following}\n"

        if location != 'N/A':
            result += f"📍 Локация: {location}\n"
        if blog:
            result += f"🌐 Website: {blog}\n"
        if twitter:
            result += f"🐦 Twitter: @{twitter}\n"

        result += f"\n🔗 https://github.com/{username}"

        return True, result

    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"


def get_weather(city: str = "Moscow") -> Tuple[bool, str]:
    """
    Получает погоду для города (через бесплатный API).

    Args:
        city: Название города

    Returns:
        (success, weather_info)
    """
    try:
        # Используем wttr.in - бесплатный API без ключа
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data.get('current_condition', [{}])[0]
        temp_c = current.get('temp_C', 'N/A')
        feels_like = current.get('FeelsLikeC', 'N/A')
        humidity = current.get('humidity', 'N/A')
        description = current.get('weatherDesc', [{}])[0].get('value', 'N/A')
        wind_speed = current.get('windspeedKmph', 'N/A')

        result = f"🌤️ <b>Погода: {city}</b>\n\n"
        result += f"🌡️ Температура: {temp_c}°C\n"
        result += f"🤔 Ощущается: {feels_like}°C\n"
        result += f"💧 Влажность: {humidity}%\n"
        result += f"💨 Ветер: {wind_speed} км/ч\n"
        result += f"☁️ Условия: {description}\n\n"
        result += f"<i>Данные от wttr.in</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Ошибка: {str(e)}"
