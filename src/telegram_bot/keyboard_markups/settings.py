from src.telegram_bot.keyboard_markups import inline_kbm

settings_layout = [
    [["🆔Изменить логин", "change_login"]],
    [["📔Изменить адрес", "change_address"]],
    [["📝Изменить описание", "change_description"]],
    [["⬅️Назад", "main_menu"]],
]
kbm_settings = inline_kbm.generate(settings_layout)
