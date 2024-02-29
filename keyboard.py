from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


weather_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton(text='Температура'), KeyboardButton(text='Влажность')],
        [KeyboardButton(text='Давление'), KeyboardButton(text='Продолжительность дня')],
        [KeyboardButton(text='Сброс')]
    ]
)
