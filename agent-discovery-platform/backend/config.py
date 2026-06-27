from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, AnyHttpUrl, SecretStr

class Settings(BaseSettings):
    # App
    ENVIRONMENT: str = "development"
    PROJECT_NAME: str = "Agent Discovery Platform"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # Database
    DATABASE_URL: PostgresDsn
    
    # Qdrant
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: Optional[SecretStr] = None
    
    # Neo4j
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: SecretStr
    
    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"
    
    # OPA
    OPA_URL: AnyHttpUrl = "http://localhost:8181" # type: ignore
    
    # AI/LLM
    OPENAI_API_KEY: SecretStr
    
    # Observability
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[SecretStr] = None
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings() # type: ignore
