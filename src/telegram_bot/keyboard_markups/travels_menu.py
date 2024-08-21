from src.telegram_bot.keyboard_markups import inline_kbm

travels_menu_layout = [
    [
        ["🧳Добавить путешествие", "add_travel"],
        ["📂Список путешествий", "list_travels"],
    ],
    [["⬅️Назад", "main_menu"]],
]
kbm_travels_menu = inline_kbm.generate(travels_menu_layout)
