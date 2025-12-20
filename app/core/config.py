from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaConfig(BaseSettings):
    servers: str = "coffee_auth_kafka:9092"


class RedisConfig(BaseSettings):
    url: str = "redis://coffee_auth_redis:6379/0"
    broker_url: str = "redis://coffee_auth_redis:6379/1"
    backend_url: str = "redis://coffee_auth_redis:6379/2"


class JwtConfig(BaseSettings):
    secret_key: str = "test-secret-key"
    algorithm: str = "HS256"
    access_expire_min: int = 15
    refresh_expire_days: int = 7


class DatabaseConfig(BaseSettings):
    host: str = "coffee_auth_db"
    port: int = 5432
    name: str = "postgres"
    user: str = "postgres"
    password: str = "postgres"

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def sync_url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class ApiConfig(BaseSettings):
    prefix: str = "/api/v1"


class Settings(BaseSettings):
    db: DatabaseConfig = DatabaseConfig()
    jwt: JwtConfig = JwtConfig()
    api: ApiConfig = ApiConfig()
    redis: RedisConfig = RedisConfig()
    kafka: KafkaConfig = KafkaConfig()

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__"
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
