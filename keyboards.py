from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
#from controller import Controller


class Buttons:
    regions = ['dada', 'nene', 'mbmb', 'any']

    select_role = InlineKeyboardMarkup()
    select_role.insert(InlineKeyboardButton(
        text="Пасажир", callback_data="passanger"))
    select_role.insert(InlineKeyboardButton(
        text="Водій", callback_data="driver"))

    def select_region(any=False):

        select_region = InlineKeyboardMarkup(row_width=2)
        regions = ['dada', 'nene', 'mbmb', 'any']  # Controller.get_regions

        for region in regions:
            select_region.add(InlineKeyboardButton(
                text=region, callback_data=regions.index(region)))
        return select_region

    def edit_drive_button(drive_id):

        edit_drive = InlineKeyboardMarkup()
        edit_drive.add(InlineKeyboardButton(
            text="Редагувати", callback_data=f'edit_{drive_id}'))
        edit_drive.add(InlineKeyboardButton(
            text="Видалити", callback_data=f"del_{drive_id}"))

        return edit_drive

    #editing data as driver
    edit_menu = InlineKeyboardMarkup(row_width=1)
    edit_menu.add(InlineKeyboardButton(
        text='Кiлькiсть пасажирiв', callback_data="pass_count"))
    edit_menu.add(InlineKeyboardButton(
        text='Дату', callback_data='date_edit'))
    edit_menu.add(InlineKeyboardButton(
        text='Коментар', callback_data='edit_com'))
    edit_menu.add(InlineKeyboardButton(
        text='Мiсце виезду', callback_data='edit_from'))
    edit_menu.add(InlineKeyboardButton(
        text='Кiнцевий пункт', callback_data='edit_to'))

    #editing data as passenger
    edit_data_menu = InlineKeyboardMarkup(row_width=2)
    edit_data_menu.insert(InlineKeyboardButton(
        text='Маршрут',callback_data=f'u_from'))
    edit_data_menu.insert(InlineKeyboardButton(
        text='Кiлькiсть', callback_data=f'u_count'))
    edit_data_menu.insert(InlineKeyboardButton(
        text="iм'я",callback_data="nm_chng"))
    #For search
    find = InlineKeyboardMarkup().insert(InlineKeyboardButton(
        text='Показати',callback_data='find_pass'))

class Keyboard:

    role_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    role_menu.add('Я Водій')
    role_menu.add('Я Пасажир')

    def menu(role):
        driver_menu = ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True,)

        if role == "Я Пасажир":
            driver_menu.add("Нотифи о новых")
            driver_menu.insert('Я Водій')
            driver_menu.add('Налаштування')
        elif role == "Я Водій":
            driver_menu.add("Мої поїздки")
            driver_menu.insert("Додати оголошення")
            driver_menu.add('Я Пасажир')

        return driver_menu
