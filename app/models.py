from app.database import Base
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
    task_type = Column(String(50), nullable=False, index=True)
    input_data = Column(Text, nullable=True)
    result = Column(Text, nullable=True)
    
    status = Column(SQLEnum(TaskStatus), index=True, default=TaskStatus.PENDING)
    priority = Column(Integer, index=True, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())