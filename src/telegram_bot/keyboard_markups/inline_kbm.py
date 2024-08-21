from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def generate(button_titles: List[List[List]]) -> InlineKeyboardMarkup:
    """
    Inline keyboard creation.
    Generating keyboard markup by inputed layout list.
    Every button must have button title and button callback.

    Exmaple:
    if there is such list
    [
        [["Hello", "start"], ["Information", "info"]],
        [["Add offer", "add_offer"], ["Del offer", "del_offer"]]
    ]
    the result inline keyabord will be with the same layout and callbacks
        Hello       Infomation
        Add offer   Del Offer
    """
    kbm_builder = InlineKeyboardBuilder()

    for row in button_titles:
        keyboard_row_buttons = []

        for button_title, button_callback in row:
            button = InlineKeyboardButton(
                text=button_title, callback_data=button_callback
            )
            keyboard_row_buttons.append(button)

        kbm_builder.row(*keyboard_row_buttons)

    return kbm_builder.as_markup(resize_keyboard=True)
