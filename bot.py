import logging
from telegram import Update
from telegram.ext import ContextTypes
from openai_service import get_chatgpt_response, INITIAL_PROMPT
from models import MessageHistory, MessageType
from db import SessionLocal
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

HISTORY_LIMIT = 10  # Количество последних сообщений для контекста

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('bot_message.txt')
welcome_template = env.get_template('welcome_message.txt')

# Определяем функцию-обработчик сообщений.
async def run_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"Received message from user: {update.effective_user.username}")
    user_message = update.message.text
    username = update.effective_user.username or update.effective_user.first_name
    
    # Если это команда /start, отправляем приветствие и завершаем обработку
    if user_message.lower() == '/start':
        welcome_message = welcome_template.render()
        await update.message.reply_text(welcome_message)
        return
    
    db = None
    response = "Извините, произошла ошибка при обработке вашего запроса."
    rendered_response = response
    
    try:
        # Инициализируем соединение с БД
        db = SessionLocal()
        
        # Сохраняем сообщение пользователя
        logger.info("Сохраняем сообщение пользователя в базу данных")
        user_msg = MessageHistory(
            username=username,
            message=user_message,
            type=MessageType.USER
        )
        db.add(user_msg)
        db.commit()
        logger.info("Сообщение пользователя успешно сохранено")
    
        # Получаем последние N сообщений пользователя и бота для истории
        logger.info("Получаем историю сообщений")
        history = db.query(MessageHistory) \
            .filter(MessageHistory.username == username) \
            .order_by(MessageHistory.create_date.desc()) \
            .limit(HISTORY_LIMIT) \
            .all()
        logger.info(f"Получено {len(history)} сообщений из истории")
            
        # История приходит в обратном порядке, разворачиваем
        history = list(reversed(history))
        
        # Формируем список сообщений для OpenAI
        openai_messages = [{"role": "system", "content": INITIAL_PROMPT}]
        for msg in history:
            role = "user" if msg.type == MessageType.USER else "assistant"
            openai_messages.append({"role": role, "content": msg.message})
        
        openai_messages.append({"role": "user", "content": user_message})
    
        # Получаем ответ от ChatGPT
        logger.info("Отправляем запрос в ChatGPT")
        response = await get_chatgpt_response(openai_messages)
        logger.info("Получен ответ от ChatGPT")
    
        # Сохраняем ответ бота
        logger.info("Сохраняем ответ бота в базу данных")
        bot_msg = MessageHistory(
            username=username,
            message=response,
            type=MessageType.BOT
        )
        db.add(bot_msg)
        db.commit()
        logger.info("Ответ бота успешно сохранен")
        
        # Рендерим шаблон сообщения бота
        logger.info("Рендеринг шаблона ответа")
        rendered_response = template.render(message=response)
        logger.info("Шаблон успешно отрендерен")
        
    except Exception as e:
        logger.error(f"Ошибка в работе бота: {e}")
        if db is not None and db.is_active:
            db.rollback()
    finally:
        # Закрываем соединение с БД
        if db is not None:
            db.close()
    
    # Отправляем ответ пользователю
    logger.info("Отправляем ответ пользователю")
    try:
        await update.message.reply_text(rendered_response)
        logger.info("Ответ успешно отправлен пользователю")
    except Exception as e:
        logger.error(f"Ошибка при отправке ответа пользователю: {e}")
