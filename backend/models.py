from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationship
    comments = relationship("Comment", back_populates="author")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    priority = Column(Integer, default=1, nullable=False)
    
    status = Column(String, default="Pending", nullable=False)
    progress = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    is_deleted = Column(Boolean, default=False, nullable=False)

    # Relationship
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="task", cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    # Relationship
    author = relationship("User", back_populates="comments")
    task = relationship("Task", back_populates="comments")

class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    original_name = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_url = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, server_default=func.now())
    is_deleted = Column(Boolean, default=False)

    # Relationship
    task = relationship("Task", back_populates="attachments")
