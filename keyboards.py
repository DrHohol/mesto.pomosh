from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
#from controller import Controller


class Buttons:
    regions = ['dada','nene','mbmb']
    
    select_role = InlineKeyboardMarkup()
    select_role.insert(InlineKeyboardButton(
        text="Пасажир", callback_data="passanger"))
    select_role.insert(InlineKeyboardButton(
        text="Водій", callback_data="driver"))

    def select_region():

        select_region = InlineKeyboardMarkup(row_width=1)
        regions = ['dada','nene','mbmb']#Controller.get_regions

        for region in regions:
            select_region.add(InlineKeyboardButton(
                text=region, callback_data=regions.index(region)))
        print(select_region)
        return select_region
        

class Keyboard:

    role_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    role_menu.add('Водій')
    role_menu.add('Пасажир')

    driver_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    driver_menu.add("Додати оголошення")
    driver_menu.add("Мої поїздки")
    print(driver_menu)