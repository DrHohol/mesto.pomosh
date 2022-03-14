from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)


class Buttons:

    select_role = InlineKeyboardMarkup()
    select_role.insert(InlineKeyboardButton(
        text="Пасажир", callback_data="passanger"))
    select_role.insert(InlineKeyboardButton(
        text="Водій", callback_data="driver"))
    