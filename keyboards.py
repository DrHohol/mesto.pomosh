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
        regions = ['dada', 'nene', 'mbmb']  # Controller.get_regions

        for region in regions:
            select_region.add(InlineKeyboardButton(
                text=region, callback_data=regions.index(region)))
        if any:
            select_region.add(InlineKeyboardButton(
                text="Пiхуй",callback_data="any"))
        return select_region

    def edit_drive_button(drive_id):

        edit_drive = InlineKeyboardMarkup()
        edit_drive.add(InlineKeyboardButton(
            text="Редагувати", callback_data=f'edit_{drive_id}'))
        edit_drive.add(InlineKeyboardButton(
            text="Видалити", callback_data=f"del_{drive_id}"))

        return edit_drive

    def cancel_passenger_button(drive_id):

        cancel_pass = InlineKeyboardMarkup()
        cancel_pass.add(InlineKeyboardButton(
            text='Вiдмiнити', callback_data=f'cancel_{drive_id}'))
        return cancel_pass

    edit_menu = InlineKeyboardMarkup(row_width=1)
    edit_menu.add(InlineKeyboardButton(
        text='Кiлькiсть пасажирiв', callback_data="pass_count"))
    edit_menu.add(InlineKeyboardButton(
        text='Дату', callback_data='date_edit'))
    edit_menu.add(InlineKeyboardButton(
        text='Коментар', callback_data='edit_com'))
    edit_menu.add(InlineKeyboardButton(
        text='Мiсце виезду', callback_data='edit_com'))
    edit_menu.add(InlineKeyboardButton(
        text='Кiнцевий пункт', callback_data='edit_com'))


class Keyboard:

    role_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    role_menu.add('Водій')
    role_menu.add('Пасажир')

    def menu(role):
        driver_menu = ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        driver_menu.add("Мої поїздки")
        if role == "Пасажир":
            driver_menu.add("Подати заявку")
            driver_menu.add("Нотифи о новых")
        elif role == "Водій":
            driver_menu.add("Додати оголошення")
        return driver_menu
