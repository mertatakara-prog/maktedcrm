from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    app_name: str = 'maktedcrm-backend'
    database_url: str = 'postgresql+psycopg2://postgres:postgres@db:5432/maktedcrm'


settings = Settings()
