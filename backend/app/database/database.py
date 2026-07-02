import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables
load_dotenv()

# Database URL
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

# Print the URL (without exposing the password)
print(
    f"Connecting to PostgreSQL: "
    f"postgresql+psycopg2://{os.getenv('DB_USER')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

try:
    # Create engine
    engine = create_engine(DATABASE_URL, echo=True)

    # Test the connection
    with engine.connect():
        print("✅ Database connected successfully!")

except Exception as e:
    print("❌ Database connection failed!")
    print(e)
    raise  # Stop the application and show the real error

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()