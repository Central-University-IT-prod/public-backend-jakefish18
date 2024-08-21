from src.telegram_bot.keyboard_markups import inline_kbm

travel_menu_layout = [
    [
        ["◀️Предыдущее", "previous_travel"],
        ["Следующее▶️", "next_travel"],
    ],
    [
        ["🗑Удалить", "delete_travel"],
        ["🌆Добавить город", "add_travel_city"],
    ],
    [["✍️Добавить заметку", "add_note"], ["🗒Заметки", "notes_menu"]],
    [
        ["🤙Поделиться путешествием", "invite_friend"],
        ["📓Удалить пользователя", "delete_friend"],
    ],
    [["⬅️Назад", "travels_menu"]],
]
kbm_travel_menu = inline_kbm.generate(travel_menu_layout)
