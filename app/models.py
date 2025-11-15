from sqlalchemy import Column, Integer, String, Text, DateTime, Enum as SQLEnum
from sqlalchemy.sql import func
import enum

class TaskStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"



class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    priority = Column(Integer, index=True)
    status = Column(Integer, index=True) # pending=0, running=1, completed=2, failed=3 (?)