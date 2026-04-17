from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PORT: int = 8000
    REDIS_URL: str = "redis://localhost:6379"
    AGENT_API_KEY: str = "dev-key-change-me"
    LOG_LEVEL: str = "INFO"
    RATE_LIMIT_PER_MINUTE: int = 20
    MONTHLY_BUDGET_USD: float = 10
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o-mini"

    class Config:
        extra = "ignore"


settings = Settings()