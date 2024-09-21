from pydantic_settings import BaseSettings

from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):

    database_url: str


settings = Settings()
