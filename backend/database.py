from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base

DATABASE_URL = "sqlite:///./taskai.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # SQLite specific
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from models import Task # Import here to avoid circular import
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database initialized successfully.")
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
