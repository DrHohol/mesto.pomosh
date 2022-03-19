from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
#from controller import Controller

class Buttons:

    regions = ["Вінницька область", "Волинська область", "Дніпропетровська область",
           "Донецька область", "Житомирська область", "Закарпатська область", "Запорізька область",
           "Івано-Франківська область", "Київська область", "Кіровоградська область", "Луганська область", "Львівська область",
           "Миколаївська область", "Одеська область", "Полтавська область", "Рівненська область", "Сумська область",
           "Тернопільська область", "Харківська область", "Херсонська область", "Хмельницька область", "Черкаська область",
           "Чернівецька область", "Чернігівська область"]

    select_role = InlineKeyboardMarkup()
    select_role.insert(InlineKeyboardButton(
        text="Пасажир", callback_data="passanger"))
    select_role.insert(InlineKeyboardButton(
        text="Водій", callback_data="driver"))

    def select_region(nowhere=False,page=1):

        select_region = InlineKeyboardMarkup(row_width=2)

        if nowhere:
            Buttons.regions.insert(0,"За кордон")
        else:
            Buttons.regions = ["Мариуполь", "Изюм", "Чугуїв", "Ахтирка",
            "Краматорськ", "Слав'янськ", "Лисичанськ"] + Buttons.regions

        if len(Buttons.regions) <= page*5+5:
            for region in Buttons.regions[page*5:]:
                select_region.add(InlineKeyboardButton(
                    text=region, callback_data=Buttons.regions.index(region)))
        else:
            for region in Buttons.regions[page*5:page*5+5]:
                select_region.add(InlineKeyboardButton(
                    text=region, callback_data=Buttons.regions.index(region)))
            select_region.add(InlineKeyboardButton(
                text='Наступна сторiнка',callback_data=f'page_{page+1}'))
        if page != 1:
            select_region.add(InlineKeyboardButton(
                text='Попередня сторiнка',callback_data=f'page_{page-1}'))
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
        text='Коментар', callback_data='com_edit'))
    edit_menu.add(InlineKeyboardButton(
        text='Маршрут', callback_data='route'))

    #editing data as passenger
    edit_data_menu = InlineKeyboardMarkup(row_width=2)
    edit_data_menu.insert(InlineKeyboardButton(
        text='Маршрут',callback_data=f'u_from'))
    edit_data_menu.insert(InlineKeyboardButton(
        text='Кiлькiсть', callback_data=f'u_count'))
    edit_data_menu.insert(InlineKeyboardButton(
        text="iм'я",callback_data="nm_chng"))
    edit_data_menu.insert(InlineKeyboardButton(
        text='Спосiб зв’язку',callback_data='ph_chng'))
    #For search
    find = InlineKeyboardMarkup().insert(InlineKeyboardButton(
        text='Показати',callback_data='find_pass'))

class Keyboard:

    role_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    role_menu.add('Надати допомогу')
    role_menu.add('Шукати допомогу')

    def menu(role):
        driver_menu = ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True,)

        if role == "Я Пасажир":
            driver_menu.add("Повідомлення")
            driver_menu.insert('Надати допомогу')
            driver_menu.add('Налаштування')
        elif role == "Я Водій":
            driver_menu.add('Налаштування')
            driver_menu.add("Мої поїздки")
            driver_menu.insert("Додати оголошення")
            driver_menu.add('Шукати допомогу')

        return driver_menu
