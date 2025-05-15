from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class MessageType(enum.Enum):
    USER = "user"
    BOT = "bot"

class MessageHistory(Base):
    __tablename__ = 'message_history'

    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    username = Column(String)
    message = Column(String)
    type = Column(Enum(MessageType))
