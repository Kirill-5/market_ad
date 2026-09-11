import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = os.getenv(
        "POSTGRES_CONNECTION_STRING",
        os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5434/ads_db"),
    ).replace("postgres://", "postgresql+asyncpg://", 1)

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"

    kafka_bootstrap_servers: str = os.getenv("KAFKA_BROKERS", os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092"))
    kafka_topic_ads: str = os.getenv("KAFKA_TOPIC_MARKETPLACE_ADS", os.getenv("KAFKA_TOPIC_ADS", "ads"))

    auth_service_url: str = os.getenv(
        "AUTH_SERVICE_URL",
        "http://student-kirill-5-marketplace-auth-service-web.student-kirill-5-marketplace-auth-service.svc.cluster.local:8000",
    )