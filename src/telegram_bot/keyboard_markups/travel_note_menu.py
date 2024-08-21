from src.telegram_bot.keyboard_markups import inline_kbm

travel_note_layout = [
    [
        ["◀️Предыдущее", "previous_note"],
        ["Следующее▶️", "next_note"],
    ],
    [
        ["🗑Удалить", "delete_note"],
    ],
    [["⬅️Назад", "list_travels"]],
]
kbm_travel_note_menu = inline_kbm.generate(travel_note_layout)
