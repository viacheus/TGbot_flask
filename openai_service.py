import logging
from openai import OpenAI
from config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

# Инициализируем клиент OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

async def get_chatgpt_response(prompt):
    """
    Отправляет запрос к ChatGPT и возвращает ответ.
    
    Args:
        prompt (str): Текст запроса пользователя
        
    Returns:
        str: Ответ от ChatGPT или сообщение об ошибке
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Error getting response from ChatGPT: {e}")
        return "Извините, произошла ошибка при обработке вашего запроса." 