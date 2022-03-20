from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
#from controller import Controller


class Buttons:

    regions_from = ["Київ", "Харків", "Чернігів", "Суми",
                    "Краматорськ", "Маріуполь", "Мелітополь", "Херсон",
                    "Миколаїв", "Одеса"]
    regions_to = ["Неважливо", "За кордон", "Бердянськ",
                  "Запоріжжя", "Дніпро", "Полтава", "Вінниця",
                  "Львів", "Івано-Франківськ", "Рівне"]

    select_role = InlineKeyboardMarkup()
    select_role.insert(InlineKeyboardButton(
        text="Пасажир", callback_data="passanger"))
    select_role.insert(InlineKeyboardButton(
        text="Водій", callback_data="driver"))

    def select_region(nowhere=False, page=0):

        select_region = InlineKeyboardMarkup(row_width=2)

        if nowhere:
            regions = Buttons.regions_to
        else:
            regions = Buttons.regions_from

        if len(regions) <= page * 5 + 5:
            print(len(regions))
            for region in regions[page * 5:]:
                select_region.add(InlineKeyboardButton(
                    text=region, callback_data=regions.index(region)))
        else:
            for region in regions[page * 5:page * 5 + 5]:
                select_region.add(InlineKeyboardButton(
                    text=region, callback_data=regions.index(region)))
            select_region.add(InlineKeyboardButton(
                text='Наступна сторiнка', callback_data=f'page_{page+1}'))
        if page != 0:
            select_region.add(InlineKeyboardButton(
                text='Попередня сторiнка', callback_data=f'page_{page-1}'))
        return select_region

    def edit_drive_button(drive_id):

        edit_drive = InlineKeyboardMarkup()
        edit_drive.add(InlineKeyboardButton(
            text="Редагувати", callback_data=f'edit_{drive_id}'))
        edit_drive.add(InlineKeyboardButton(
            text="Видалити", callback_data=f"del_{drive_id}"))

        return edit_drive

    # editing data as driver
    edit_menu = InlineKeyboardMarkup(row_width=1)
    edit_menu.add(InlineKeyboardButton(
        text='Маршрут', callback_data='route'))
    edit_menu.add(InlineKeyboardButton(
        text='Кiлькiсть пасажирiв', callback_data="pass_count"))
    edit_menu.add(InlineKeyboardButton(
        text='Коментар', callback_data='com_edit'))
    edit_menu.add(InlineKeyboardButton(
        text='Дату', callback_data='date_edit'))


    # editing data as passenger
    edit_data_menu = InlineKeyboardMarkup(row_width=2)
    edit_data_menu.insert(InlineKeyboardButton(
        text='Маршрут', callback_data=f'u_from'))
    edit_data_menu.insert(InlineKeyboardButton(
        text='Кiлькiсть пасажирiв', callback_data=f'u_count'))
    edit_data_menu.insert(InlineKeyboardButton(
        text="iм'я", callback_data="nm_chng"))
    edit_data_menu.insert(InlineKeyboardButton(
        text='Спосiб зв’язку', callback_data='ph_chng'))
    # For search
    find = InlineKeyboardMarkup().insert(InlineKeyboardButton(
        text='Показати', callback_data='find_pass'))


class Keyboard:

    role_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    role_menu.add('Надати допомогу')
    role_menu.add('Шукати допомогу')

    skip = ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True).add(
        "Пропустити")

    def menu(role):
        driver_menu = ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True,)

        if role == "Я Пасажир":
            driver_menu.add("Вимкнути повідомлення")
            driver_menu.insert('Надати допомогу')
            driver_menu.add('Редагувати поїздки')
        elif role == "Я Водій":
            driver_menu.add("Додати оголошення")
            driver_menu.insert("Мої поїздки")
            driver_menu.add('Змінити маршрут')
            driver_menu.insert('Шукати допомогу')

        return driver_menu
