import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    # Server settings
    server_host: str = f'{os.environ.get("SERVER_HOST")}'
    server_port: int = os.environ.get("SERVER_PORT")

    # Database settings
    database_url: str = f'postgresql+psycopg2' \
                        f'://{os.environ.get("POSTGRES_USER")}' \
                        f':{os.environ.get("POSTGRES_PASSWORD")}' \
                        f'@{os.environ.get("POSTGRES_HOST")}' \
                        f'/{os.environ.get("POSTGRES_NAME")}'

    # JWT Settings
    jwt_algorithm: str = 'HS256'
    jwt_expiration: int = 3600  # Seconds
    jwt_secret: str = f'{os.environ.get("JWT_SECRET")}'


settings = Settings()
