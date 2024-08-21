from environs import Env

# .env file must be placed in src/ folder
env = Env()


class Settings:
    # Bot settings.
    BOT_TOKEN: str = env("BOT_TOKEN", "EMPTY_BOT_TOKEN")
    STORAGE_PATH: str = env("STORAGE_PATH", "/output")
    BOT_ANSWERS_PATH: str = env(
        "BOT_ANSWERS_PATH", "/src/telegram_bot/message_markdowns"
    )
    IS_TEST_SETTINGS: bool = env("IS_TEST_SETTINGS", False)

    # Database settings.
    SQLALCHEMY_DATABASE_URI: str = env("POSTGRES_CONN")


settings = Settings()
