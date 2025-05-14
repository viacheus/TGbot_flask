# Импортируем необходимые классы.
import logging
from telegram.ext import Application, MessageHandler, filters
from telegram import Update
from telegram.ext import ContextTypes
from config import BOT_TOKEN
from openai_service import get_chatgpt_response
from models import MessageHistory, MessageType
from db import init_db, SessionLocal

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

HISTORY_LIMIT = 10  # Количество последних сообщений для контекста

# Определяем функцию-обработчик сообщений.
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    username = update.effective_user.username or update.effective_user.first_name
    
    # Сохраняем сообщение пользователя
    db = SessionLocal()
    try:
        user_msg = MessageHistory(
            username=username,
            message=user_message,
            type=MessageType.USER
        )
        db.add(user_msg)
        db.commit()
    finally:
        db.close()

    # Получаем последние N сообщений пользователя и бота для истории
    db = SessionLocal()
    try:
        history = db.query(MessageHistory) \
            .filter(MessageHistory.username == username) \
            .order_by(MessageHistory.create_date.desc()) \
            .limit(HISTORY_LIMIT) \
            .all()
    finally:
        db.close()
    # История приходит в обратном порядке, разворачиваем
    history = list(reversed(history))
    # Формируем список сообщений для OpenAI
    openai_messages = []
    for msg in history:
        role = "user" if msg.type == MessageType.USER else "assistant"
        openai_messages.append({"role": role, "content": msg.message})
    # Добавляем текущее сообщение пользователя (на всякий случай)
    openai_messages.append({"role": "user", "content": user_message})

    # Отправляем историю в ChatGPT
    response = await get_chatgpt_response(openai_messages)

    # Сохраняем ответ бота
    db = SessionLocal()
    try:
        bot_msg = MessageHistory(
            username=username,
            message=response,
            type=MessageType.BOT
        )
        db.add(bot_msg)
        db.commit()
    finally:
        db.close()
    
    # Отправляем ответ пользователю
    await update.message.reply_text(response)


def main():
    # Инициализируем базу данных
    init_db()
    
    # Создаём объект Application.
    # Вместо слова "TOKEN" надо разместить полученный от @BotFather токен
    application = Application.builder().token(BOT_TOKEN).build()

    # Создаём обработчик сообщений типа filters.TEXT
    # из описанной выше асинхронной функции echo()
    # После регистрации обработчика в приложении
    # эта асинхронная функция будет вызываться при получении сообщения
    # с типом "текст", т. е. текстовых сообщений.
    text_handler = MessageHandler(filters.TEXT, echo)

    # Регистрируем обработчик в приложении.
    application.add_handler(text_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()