from src.core import settings

def get(filename: str) -> str:
    """
    Returning file content which lies inside given file.

    Parameters:
        filename: str - filename to get file

    Returns:
        str - file content
    """
    with open(f"{settings.BOT_ANSWERS_PATH}/{filename}.html", encoding="utf-8", mode="r") as file:
        return file.read()