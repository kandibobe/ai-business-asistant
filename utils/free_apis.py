"""
Free API integrations for developers.
All APIs don't require API keys or have generous free limits.
"""
import requests
from typing import Dict, Any, List, Tuple
from datetime import datetime


def search_github_repos(query: str, limit: int = 5) -> Tuple[bool, str]:
    """
    Search GitHub repositories (without API key).

    Args:
        query: Search query
        limit: Number of results (max 10)

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
            return False, f"❌ No repositories found for '{query}'"

        result = f"🔍 <b>GitHub: found {data.get('total_count', 0):,} repositories</b>\n\n"
        result += f"<b>Top {len(repos)} results:</b>\n\n"

        for i, repo in enumerate(repos, 1):
            name = repo.get('full_name', 'N/A')
            description = repo.get('description', 'No description')[:100]
            stars = repo.get('stargazers_count', 0)
            language = repo.get('language', 'N/A')
            url = repo.get('html_url', '')

            result += f"{i}. <b>{name}</b>\n"
            result += f"   ⭐ {stars:,} | 💻 {language}\n"
            result += f"   📝 {description}\n"
            result += f"   🔗 {url}\n\n"

        return True, result

    except requests.RequestException as e:
        return False, f"❌ Request error: {str(e)}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def search_npm_package(query: str) -> Tuple[bool, str]:
    """
    Search NPM packages.

    Args:
        query: Package name

    Returns:
        (success, result_message)
    """
    try:
        url = f"https://registry.npmjs.org/{query}"
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            return False, f"❌ Package '{query}' not found on NPM"

        response.raise_for_status()
        data = response.json()

        # Get latest version
        latest_version = data.get('dist-tags', {}).get('latest', 'N/A')
        description = data.get('description', 'No description')
        homepage = data.get('homepage', 'N/A')
        repo_url = data.get('repository', {})
        if isinstance(repo_url, dict):
            repo_url = repo_url.get('url', 'N/A')

        # Get version info
        versions = data.get('versions', {})
        latest_info = versions.get(latest_version, {})

        result = f"📦 <b>NPM Package: {query}</b>\n\n"
        result += f"🏷️ Latest version: <code>{latest_version}</code>\n"
        result += f"📝 Description: {description}\n\n"

        # Dependencies
        dependencies = latest_info.get('dependencies', {})
        if dependencies:
            result += f"📚 Dependencies: {len(dependencies)}\n"

        # Keywords
        keywords = data.get('keywords', [])
        if keywords:
            result += f"🏷️ Tags: {', '.join(keywords[:5])}\n"

        result += f"\n🌐 Homepage: {homepage}\n"
        result += f"📂 Repo: {repo_url}\n"
        result += f"📥 Install: <code>npm install {query}</code>"

        return True, result

    except requests.RequestException as e:
        return False, f"❌ Request error: {str(e)}"
    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def check_browser_support(feature: str) -> Tuple[bool, str]:
    """
    Checks web feature browser support via Can I Use API.

    Args:
        feature: Feature name (e.g., 'flexbox', 'css-grid')

    Returns:
        (success, result_message)
    """
    try:
        # Use public caniuse API
        url = f"https://caniuse.com/process/query"
        params = {'search': feature}

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        # Alternative approach - use static data
        result = f"🌐 <b>Browser Support: {feature}</b>\n\n"
        result += f"🔍 Check full information:\n"
        result += f"🔗 https://caniuse.com/?search={feature}\n\n"
        result += f"💡 <i>For detailed browser support information,\n"
        result += f"visit Can I Use via link above</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def get_public_ip() -> Tuple[bool, str]:
    """Gets public IP address"""
    try:
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        response.raise_for_status()
        data = response.json()
        ip = data.get('ip', 'N/A')

        result = f"🌐 <b>Your public IP:</b>\n\n"
        result += f"<code>{ip}</code>\n\n"
        result += f"💡 <i>This is bot's IP, not user's</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def get_random_quote() -> Tuple[bool, str]:
    """Gets random motivational quote"""
    try:
        response = requests.get('https://api.quotable.io/random', timeout=5)
        response.raise_for_status()
        data = response.json()

        quote = data.get('content', '')
        author = data.get('author', 'Unknown')

        result = f"💭 <b>Quote of the Day:</b>\n\n"
        result += f"<i>\"{quote}\"</i>\n\n"
        result += f"— <b>{author}</b>"

        return True, result

    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def get_random_joke() -> Tuple[bool, str]:
    """Gets random programmer joke"""
    try:
        response = requests.get('https://official-joke-api.appspot.com/random_joke', timeout=5)
        response.raise_for_status()
        data = response.json()

        setup = data.get('setup', '')
        punchline = data.get('punchline', '')

        result = f"😄 <b>Programmer Joke:</b>\n\n"
        result += f"{setup}\n\n"
        result += f"<i>{punchline}</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def get_crypto_price(crypto: str = 'bitcoin') -> Tuple[bool, str]:
    """
    Gets current cryptocurrency price.

    Args:
        crypto: Crypto name (bitcoin, ethereum, etc)

    Returns:
        (success, result_message)
    """
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price"
        params = {
            'ids': crypto.lower(),
            'vs_currencies': 'usd,eur',
            'include_24hr_change': 'true'
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if crypto.lower() not in data:
            return False, f"❌ Cryptocurrency '{crypto}' not found"

        crypto_data = data[crypto.lower()]
        price_usd = crypto_data.get('usd', 0)
        price_eur = crypto_data.get('eur', 0)
        change_24h = crypto_data.get('usd_24h_change', 0)

        change_icon = "📈" if change_24h > 0 else "📉"
        change_color = "+" if change_24h > 0 else ""

        result = f"💰 <b>{crypto.capitalize()} Price</b>\n\n"
        result += f"💵 ${price_usd:,.2f}\n"
        result += f"💶 €{price_eur:,.2f}\n\n"
        result += f"{change_icon} 24h: {change_color}{change_24h:.2f}%\n\n"
        result += f"<i>Data from CoinGecko</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def generate_qr_code(text: str) -> Tuple[bool, str]:
    """
    Generates QR code link.

    Args:
        text: Text for QR code

    Returns:
        (success, url_to_qr_code)
    """
    try:
        from urllib.parse import quote
        encoded_text = quote(text)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={encoded_text}"

        result = f"📱 <b>QR Code generated!</b>\n\n"
        result += f"🔗 URL: {qr_url}\n\n"
        result += f"💡 <i>Open the link to see QR code</i>"

        return True, qr_url

    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def shorten_url(long_url: str) -> Tuple[bool, str]:
    """
    Shortens URL via free service.

    Args:
        long_url: Long URL

    Returns:
        (success, short_url)
    """
    try:
        # Use is.gd - free without API key
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
            result = f"🔗 <b>URL shortened!</b>\n\n"
            result += f"📎 Original: <code>{long_url[:50]}...</code>\n"
            result += f"✂️ Short: <code>{short_url}</code>\n\n"
            result += f"💡 <i>Copy the short link</i>"

            return True, result
        else:
            return False, "❌ Failed to shorten URL"

    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def get_github_user_info(username: str) -> Tuple[bool, str]:
    """
    Gets GitHub user information.

    Args:
        username: GitHub username

    Returns:
        (success, user_info)
    """
    try:
        url = f"https://api.github.com/users/{username}"
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            return False, f"❌ User '{username}' not found"

        response.raise_for_status()
        data = response.json()

        name = data.get('name', username)
        bio = data.get('bio', 'No bio')
        public_repos = data.get('public_repos', 0)
        followers = data.get('followers', 0)
        following = data.get('following', 0)
        location = data.get('location', 'N/A')
        blog = data.get('blog', '')
        twitter = data.get('twitter_username', '')

        result = f"👤 <b>GitHub: {name}</b>\n\n"
        result += f"🆔 Username: <code>{username}</code>\n"
        result += f"📝 Bio: {bio}\n\n"
        result += f"📦 Repositories: {public_repos}\n"
        result += f"👥 Followers: {followers}\n"
        result += f"👤 Following: {following}\n"

        if location != 'N/A':
            result += f"📍 Location: {location}\n"
        if blog:
            result += f"🌐 Website: {blog}\n"
        if twitter:
            result += f"🐦 Twitter: @{twitter}\n"

        result += f"\n🔗 https://github.com/{username}"

        return True, result

    except Exception as e:
        return False, f"❌ Error: {str(e)}"


def get_weather(city: str = "Moscow") -> Tuple[bool, str]:
    """
    Gets weather for a city (via free API).

    Args:
        city: City name

    Returns:
        (success, weather_info)
    """
    try:
        # Use wttr.in - free API without key
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

        result = f"🌤️ <b>Weather: {city}</b>\n\n"
        result += f"🌡️ Temperature: {temp_c}°C\n"
        result += f"🤔 Feels like: {feels_like}°C\n"
        result += f"💧 Humidity: {humidity}%\n"
        result += f"💨 Wind: {wind_speed} km/h\n"
        result += f"☁️ Conditions: {description}\n\n"
        result += f"<i>Data from wttr.in</i>"

        return True, result

    except Exception as e:
        return False, f"❌ Error: {str(e)}"
