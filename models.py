from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import declarative_base
import enum

# Create base class for declarative models
Base = declarative_base()

# Create enum for message type
class MessageType(enum.Enum):
    USER = "user"
    BOT = "bot"

# Message history model
class MessageHistory(Base):
    __tablename__ = 'message_history'

    id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=datetime.utcnow)
    username = Column(String)
    message = Column(String)
    type = Column(Enum(MessageType)) 