import os
import logging
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Debug: Print all environment variables
logger.debug("All environment variables: %s", dict(os.environ))

BOT_TOKEN = os.environ["TG_BOT_TOKEN"]
logger.debug("BOT_TOKEN found: %s", bool(BOT_TOKEN))

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
logger.debug("OPENAI_API_KEY found: %s", bool(OPENAI_API_KEY))