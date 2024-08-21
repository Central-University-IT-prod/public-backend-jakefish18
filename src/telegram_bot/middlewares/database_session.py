from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.database import SessionLocal


class DatabaseSessionMiddleware(BaseMiddleware):
    """Middleware for passing database session to handlers."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        with SessionLocal() as db:
            data["db"] = db
            return await handler(event, data)
