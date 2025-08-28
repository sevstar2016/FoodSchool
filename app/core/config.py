from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = Field(default="FoodAPI")
    debug: bool = Field(default=False)

    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default="food")
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="postgres")

    jwt_secret: str = Field(default="devsecret")
    jwt_algorithm: str = Field(default="HS256")
    jwt_exp_minutes: int = Field(default=60)

    admin_email: str = Field(default="admin@example.com")
    admin_password: str = Field(default="admin")
    admin_phone: str = Field(default="0000000000")
    admin_avatar_url: str = Field(default="")

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


