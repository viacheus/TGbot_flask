import logging
from openai import OpenAI
from config import OPENAI_API_KEY
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

# Инициализируем клиент OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Рендерим системный промпт из шаблона
env = Environment(loader=FileSystemLoader('templates'))
INITIAL_PROMPT = env.get_template('system_prompt.txt').render()

async def get_chatgpt_response(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Ошибка при получении ответа от ChatGPT: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса." 