from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() 

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(Integer, default=1, nullable=False)
    
    status = Column(String, default="Pending", nullable=False)  # Status: Pending, In Progress, Completed
    progress = Column(Integer, default=0, nullable=False)  # Progress dalam persen (0-100)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    is_deleted = Column(Boolean, default=False, nullable=False)
