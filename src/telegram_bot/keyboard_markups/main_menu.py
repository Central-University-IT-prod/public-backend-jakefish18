from src.telegram_bot.keyboard_markups import inline_kbm

main_menu_layout = [
    [["🌍Мои путешествия", "travels_menu"]],
    [["ℹ️Информация", "get_info"], ["⚙️Настройки", "settings"]],
]
kbm_main_menu = inline_kbm.generate(main_menu_layout)
