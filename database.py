import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Get database URL from environment variables (Railway MySQL)
# Railway provides multiple MySQL connection variables
DATABASE_URL = os.getenv("MYSQL_PUBLIC_URL") or os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL")

# Fallback to default for local development
if not DATABASE_URL:
    DATABASE_URL = "mysql+pymysql://user:password@localhost/dbname"

# For Railway MySQL, we need to handle SSL configuration
if DATABASE_URL and DATABASE_URL.startswith("mysql://"):
    # Convert mysql:// to mysql+pymysql:// for Railway
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)
    
    # Add SSL configuration for Railway MySQL
    if "?" not in DATABASE_URL:
        DATABASE_URL += "?ssl_verify_cert=false"
    else:
        DATABASE_URL += "&ssl_verify_cert=false"

# Create SQLAlchemy engine with connection pooling for production
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 