import asyncio
import sys

from environs import Env

env = Env()
sys.path.append(env("PATH_TO_PROJECT"))

from src import telegram_bot

if __name__ == "__main__":
    asyncio.run(telegram_bot.run_bot())
