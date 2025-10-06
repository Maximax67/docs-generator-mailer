from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_TITLE: str = "Docs Generator"
    API_TOKEN: str

    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USERNAME: str
    SMTP_PASSWORD: SecretStr
    SMTP_USE_TLS: bool = True
    SMTP_FROM_EMAIL: str

    EMAIL_VERIFICATION_TEMPLATE: str = "./app/mail/confirm.handlebars"
    PASSWORD_RESET_TEMPLATE: str = "./app/mail/reset-password.handlebars"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings(**{})
