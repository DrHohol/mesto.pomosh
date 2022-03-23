from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

# from controller import Controller


class Buttons:

    regions = ['Неважливо', 'За кордон', 'Вінниця', 'Дніпро', 'Донецьк', 'Житомир', 'Запоріжжя', 'Івано-Франківськ', 'Київ', 'Кропівницький', '', 'Луцьк', 'Львів', 'Миколаїв', 'Одеса',
        'Полтава', 'Рівне', 'Суми', 'Тернопіль', 'Ужгород', 'Харків', 'Херсон', 'Хмельницький', 'Черкаси', 'Чернігів', 'Чернівці', 'Крим', 'Бердянськ', 'Маріуполь', 'Мелітополь']

    select_role = InlineKeyboardMarkup()
    select_role.insert(InlineKeyboardButton(
        text="Пасажир", callback_data="passanger"))
    select_role.insert(InlineKeyboardButton(
        text="Водій", callback_data="driver"))


    def edit_drive_button(drive_id):

        edit_drive = InlineKeyboardMarkup()
        edit_drive.add(
            InlineKeyboardButton(
                text="Редагувати", callback_data=f"edit_{drive_id}")
        )
        edit_drive.add(
            InlineKeyboardButton(
                text="Видалити", callback_data=f"del_{drive_id}")
        )

        return edit_drive

    # editing data as driver
    edit_menu = InlineKeyboardMarkup(row_width=1)
    edit_menu.add(InlineKeyboardButton(text="Маршрут", callback_data="route"))
    edit_menu.add(
        InlineKeyboardButton(text="Кiлькiсть пасажирiв",
                             callback_data="pass_count")
    )
    edit_menu.add(InlineKeyboardButton(
        text="Коментар", callback_data="com_edit"))
    edit_menu.add(InlineKeyboardButton(text="Дату", callback_data="date_edit"))

    # editing data as passenger
    edit_data_menu = InlineKeyboardMarkup(row_width=2)
    edit_data_menu.insert(InlineKeyboardButton(
        text="Маршрут", callback_data=f"u_from"))
    edit_data_menu.insert(
        InlineKeyboardButton(text="Кiлькiсть пасажирiв",
                             callback_data=f"u_count")
    )
    edit_data_menu.insert(InlineKeyboardButton(
        text="iм'я", callback_data="nm_chng"))
    edit_data_menu.insert(
        InlineKeyboardButton(text="Спосiб зв’язку", callback_data="ph_chng")
    )
    # For search
    find = InlineKeyboardMarkup().insert(
        InlineKeyboardButton(text="Показати", callback_data="find_pass")
    )

    regularbtn = InlineKeyboardMarkup().add(InlineKeyboardButton(
        text='Регулярно', callback_data='regular'))


class Keyboard:

    role_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    role_menu.add("Надати допомогу")
    role_menu.add("Шукати допомогу")

    skip = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        "Пропустити"
    )

    def menu(role):
        driver_menu = ReplyKeyboardMarkup(
            resize_keyboard=True,
            one_time_keyboard=True,
        )

        if role == "Я Пасажир":
            driver_menu.add("Вимкнути повідомлення")
            driver_menu.insert("Надати допомогу")
            driver_menu.add("Змінити маршрут")
        elif role == "Я Водій":
            driver_menu.add("Додати оголошення")
            driver_menu.insert("Мої поїздки")
            driver_menu.add("Редагувати інформацію")
            driver_menu.insert("Шукати допомогу")

        return driver_menu

    def regions_kb(anywhere=False):
        reg_kb = ReplyKeyboardMarkup(one_time_keyboard=True,
                                     resize_keyboard=True)
        for region in Buttons.regions:
            reg_kb.add(region)

        return reg_kb
