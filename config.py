import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
