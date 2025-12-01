from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str
    secret_key: str = "your-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    gmail_email: str
    gmail_app_password: str

    model_config = SettingsConfigDict(env_file=".env", extra='allow')

settings = Settings()


