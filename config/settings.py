import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "book_scraping")

    # RabbitMQ
    RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://admin:password123@localhost:5672/")

    # API Configuration
    API_TITLE = os.getenv("API_TITLE", "Book Scraping API")
    API_DESCRIPTION = os.getenv("API_DESCRIPTION", "API for managing book scraping operations")
    API_VERSION = os.getenv("API_VERSION", "1.0.0")

    # Server Configuration
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))

    # CORS Configuration
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Environment
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()