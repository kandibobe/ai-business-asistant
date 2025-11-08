# check_models.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# Настройка логирования для более чистого вывода
logging.basicConfig(level=logging.INFO, format='%(message)s')

def check_available_models():
    """
    Подключается к API Google и выводит список доступных моделей,
    подходящих для нашего чат-бота.
    """
    try:
        # Загружаем API ключ из .env файла
        load_dotenv()
        api_key = os.getenv('GEMINI_API_KEY')

        if not api_key:
            logging.error("❌ Ошибка: Не удалось найти GEMINI_API_KEY в файле .env")
            return

        genai.configure(api_key=api_key)

        logging.info("🔍 Проверяем доступные модели для вашего API ключа...")
        logging.info("=" * 50)
        
        found_models = False
        # Проходим по всем моделям, доступным для ключа
        for model in genai.list_models():
            # Нам нужны только те модели, которые поддерживают наш основной метод 'generateContent'
            if 'generateContent' in model.supported_generation_methods:
                logging.info(f"✅ Найдена подходящая модель:")
                logging.info(f"  - Имя для API (model.name):         {model.name}")
                logging.info(f"  - Отображаемое имя (display_name): {model.display_name}")
                logging.info(f"  - Лимит токенов на входе:         {model.input_token_limit}")
                logging.info(f"  - Лимит токенов на выходе:        {model.output_token_limit}")
                logging.info("-" * 50)
                found_models = True
        
        if not found_models:
            logging.warning("Не найдено ни одной модели, поддерживающей 'generateContent'.")
            
    except Exception as e:
        logging.error(f"Произошла критическая ошибка при подключении к API Google: {e}")

if __name__ == "__main__":
    check_available_models()