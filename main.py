import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from db import init_db
from bot import run_bot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

def main():
    init_db()
    
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Обработчик для команды /start
    start_handler = CommandHandler('start', run_bot)
    application.add_handler(start_handler)
    
    # Обработчик для всех текстовых сообщений
    text_handler = MessageHandler(filters.TEXT, run_bot)
    application.add_handler(text_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()
