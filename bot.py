from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv
from keyboards import Buttons, Keyboard
from states import States
import database.controller as controller
from datetime import datetime
from database.models import Drive
from utils import generate_info
import os

load_dotenv()

bot = Bot(token=os.environ.get("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["help", "start"], state="*")
async def hello(message: types.Message):
    await message.answer(
        "Привiт! Цей бот допоможе вам евакуюватись до безпечного мiсця")
    if controller.get_or_create_user(message.from_user.id)[1]:
        await message.answer("Щоб продовжити введiть iнформацiю про себе. Почнемо з iм'я:")
        await States.set_name.set()
    else:
        await message.answer("Хто ви?",
                             reply_markup=Keyboard.role_menu)


@dp.callback_query_handler(state=States.choose_role)
async def choose_role(callback_query: types.CallbackQuery, state: FSMContext):
    #user = Controller.user_exist()
    # async with state.proxy() as data:
                #data['chat_id'] = callback_query.chat.id
    await States.set_name.set()


@dp.message_handler(state=States.set_name)
async def choose_role(message: types.Message, state: FSMContext):
    user = controller.get_or_create_user(
        message.from_user.id)[0]
    
    if not user.contact_info:
        async with state.proxy() as data:
            data['name'] = message.text
            data['uid'] = message.from_user.id
        await States.set_number.set()
        await message.answer("Додайте спосiб зв'язку")
    else:
        await message.answer('iнформацiю оновлено')
        controller.edit_user(user,
            {'name': message.text})
        await state.finish()


@dp.message_handler(state=States.set_number)
async def choose_role(message: types.Message, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await States.set_number.set()
    await message.answer(f"""
Вашi даннi:
Iм'я: {data['name']}
Спосiб зв'язку: {data['phone_number']}""",
                         reply_markup=Keyboard.role_menu)
    controller.edit_user(controller.get_or_create_user(data['uid'])[0],
                         {'name': data['name'], 'contact_info': data['phone_number']})
    await state.finish()
""" For driver """


@dp.message_handler(Text(equals="Я Водій"))
async def set_driver_menu(message: types.Message, state: FSMContext):
    await message.answer("Добре! Що ви хочете зробити?", reply_markup=Keyboard.menu('Я Водій'))


@dp.message_handler(Text(equals="Додати оголошення"), state="*")
async def set_driver_menu(message: types.Message, state: FSMContext):
    await message.answer("Какой-то биг текст с уточнениями. Выберите начальный пункт",
                         reply_markup=Buttons.select_region())
    await States.from_drive.set()


@dp.callback_query_handler(state=States.from_drive)
async def choose_role(callback_query: types.CallbackQuery, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
        data['drive_from'] = callback_query.data
    await States.to_drive.set()
    await callback_query.message.edit_text("Добре, тепер куди",
                                           reply_markup=Buttons.select_region())
    await callback_query.answer()


@dp.callback_query_handler(state=States.to_drive)
async def choose_role(callback_query: types.CallbackQuery, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
        data['drive_to'] = callback_query.data
    await callback_query.message.answer("Скiльки пассажирiв ви можете взяти?")
    await callback_query.answer()
    await States.max_pass.set()


@dp.message_handler(state=States.max_pass)
async def set_driver_menu(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit() and int(message.text) >= 1:
            data['max_pass'] = int(message.text)
            await message.answer("Коментар (необяз)")
            await States.comment.set()
        else:
            await message.answer("Помилка. Можна лише числа >= 1")


@dp.message_handler(state=States.comment)
async def set_date(message: types.Message, state: FSMContext):
    async with state.proxy() as data:

        data['comment'] = message.text
        await message.answer("Тепер вкажiть дату у\
форматi ДД.ММ.РР ГГ:ХХ")
        await States.date.set()


@dp.message_handler(state=States.date)
async def add_drive(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['date'] = datetime.strptime(message.text, "%d.%m.%y %H:%M")
        except Exception as e:
            print(e)
            await message.answer(f"Wrong format")
            print(data['date'])
    await message.answer(f"""Поїздка запланована на: {data['date']}
Початковый пункт: {Buttons.regions[int(data['drive_from'])]}
Кiнечний пункт: {Buttons.regions[int(data['drive_to'])]}
Пасажирiв: {data['max_pass']}
Коментар: {data['comment']}""")
    controller.create_drive(Buttons.regions[int(data['drive_from'])],
                            Buttons.regions[int(data['drive_to'])],
                            message.from_user.id,
                            data['max_pass'],
                            data['date'],
                            data['comment'])
    await send_notify(data)
    await state.finish()


async def send_notify(data):
    users = controller.get_user_by(
        Buttons.regions[int(data['drive_from'])],
        Buttons.regions[int(data['drive_to'])],
        data['max_pass'])
    print(users)
    if users:
        for user in users:
            await bot.send_message(
                user.chat_id,
                text=f"""Поїздка запланована на:{data['date']}
Початковый пункт: {Buttons.regions[int(data['drive_from'])]}
Кiнечний пункт: {Buttons.regions[int(data['drive_to'])]}
Пасажирiв: {data['max_pass']}
Коментар: {data['comment']}""")
    # print(users[0].name)


@dp.message_handler(Text(equals="Мої поїздки"))
async def my_drives(message: types.Message, state: FSMContext):
    user = controller.get_or_create_user(message.from_user.id)[0]
    print(user.id)
    drives = controller.get_drive_by({Drive.driver_id: user.id})
    for drive in drives:
        await message.answer(generate_info(drive),
                             reply_markup=Buttons.edit_drive_button(drive.id))
    del drives
    #drives = Controller.get_drives


@dp.callback_query_handler(Text(startswith="del"), state="*")
async def delete_drive(callback_query: types.CallbackQuery, state: FSMContext):
    drive_id = callback_query.data.split('_')[1]
    controller.delete_drive(controller.get_drive_by(
        {Drive.id: drive_id})[0])
    await callback_query.message.edit_text("Видалено")
    await callback_query.answer()


@dp.callback_query_handler(Text(startswith="edit"), state="*")
async def edit_drive(callback_query: types.CallbackQuery, state: FSMContext):
    drive_id = callback_query.data.split('_')[1]
    await callback_query.message.answer('Що ви хочете змiнити?',
                                        reply_markup=Buttons.edit_menu)
    await callback_query.answer()

'''For user'''


@dp.message_handler(Text(equals="Я Пасажир"), state="*")
async def passenger_menu(message: types.Message):
    await message.answer("В настройках уже указаны точки, надо изменить будет",
                         reply_markup=Keyboard.menu("Я Пасажир"))
    user = controller.get_or_create_user(message.from_user.id)[0]
    if not user.place_from:
        await message.answer("Де ви?",
                             reply_markup=Buttons.select_region())
        await States.settings_from.set()
    else:

        drives = controller.get_drive_by({
            Drive.place_from: user.place_from,
            Drive.place_to: user.place_to},
            places=user.num_of_passengers)
        for drive in drives:
            await callback_query.message.answer(
                generate_info(drive))


@dp.callback_query_handler(state=States.settings_from)
async def set_start(callback_query: types.CallbackQuery, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
        data['drive_from'] = callback_query.data
    await callback_query.message.edit_text("Добре, тепер куди вам треба",
                                           reply_markup=Buttons.select_region(any=True))
    await callback_query.answer()
    await States.settings_to.set()


@dp.callback_query_handler(state=States.settings_to)
async def set_finish(callback_query: types.CallbackQuery, state: FSMContext):

    await callback_query.answer()
    async with state.proxy() as data:
        data['drive_to'] = callback_query.data

    user = controller.get_or_create_user(
        callback_query.from_user.id)[0]
    if user.num_of_passengers:
        controller.edit_user(user,
            {'place_from': Buttons.regions[int(data['drive_from'])],
            'place_to': Buttons.regions[int(callback_query.data)]})
        await callback_query.message.edit_text("Оновлено!",
            reply_markup=Buttons.find)
        await state.finish()

    else:
        await callback_query.message.edit_text("Скiльки людей",
                                           reply_markup=None)
        await States.settings_pass.set()


@dp.message_handler(state=States.settings_pass)
async def get_drives(message: types.Message, state: FSMContext):

    user = controller.get_or_create_user(message.from_user.id)[0]

    if user.place_from:
        controller.edit_user(user,
            {'num_of_passengers':int(message.text)})
        await message.answer("iнформацiю оновлено. Показати оголошення?",
            reply_markup=Buttons.find)
        await state.finish()
    else:
        async with state.proxy() as data:
            controller.edit_user(user,
                {'place_from': Buttons.regions[int(data['drive_from'])],
                 'place_to': Buttons.regions[int(data['drive_to'])],
                 'num_of_passengers': int(message.text)})

        await message.answer("Инфо есть. ща подборка")
        await state.finish()
        drives = controller.get_drive_by({
            Drive.place_from: Buttons.regions[int(data['drive_from'])],
            Drive.place_to: Buttons.regions[int(data['drive_to'])]},
            places=int(message.text))
        for drive in drives:
            await message.answer(
                generate_info(drive))

@dp.callback_query_handler(Text(equals='find_pass'))
async def choose_role(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user = controller.get_or_create_user(callback_query.from_user.id)[0]
    drives = controller.get_drive_by({
            Drive.place_from: user.place_from,
            Drive.place_to: user.place_to},
            places=user.num_of_passengers)
    await callback_query.message.delete()
    if not drives:
        await bot.send_message(
            callback_query.from_user.id,
            "Нажаль зараз нема поїздок для вас")
    for drive in drives:
        await bot.send_message(
            callback_query.from_user.id,
            generate_info(drive))


@dp.message_handler(Text(equals="Налаштування"))
async def settings(message: types.Message, state: FSMContext):
    await message.answer("Шо змiнити хочете",
                         reply_markup=Buttons.edit_data_menu)

@dp.message_handler(Text(equals="Нотифи о новых"))
async def notify(message: types.Message):
    user = controller.get_or_create_user(message.from_user.id)[0]
    if user.active_search:
        controller.edit_user(user,
            {'active_search':False})
        await message.answer("Нотифи выкл",
                         reply_markup=Keyboard.menu("Я Пасажир"))
    else:
        controller.edit_user(user,
            {'active_search':True})
        await message.answer("Нотифи вкл",
            reply_markup=Keyboard.menu("Я Пасажир"))


""" Editing user info """
@dp.callback_query_handler(Text(equals='nm_chng'))
async def change_name(callback_query: types.CallbackQuery, state: FSMContext):

    await callback_query.message.answer("Введiть нове iм'я")
    callback_query.answer()
    await States.set_name.set()

@dp.callback_query_handler(Text(equals='u_count'))
async def change_pass_count(callback_query: types.CallbackQuery):

    await callback_query.message.answer("Введiть Скiльки вас")
    await callback_query.answer()
    await States.settings_pass.set()

@dp.callback_query_handler(Text(equals='u_from'))
async def change_pass_count(callback_query: types.CallbackQuery):

    await callback_query.message.answer("Оберiть точку виiзду",
        reply_markup=Buttons.select_region())
    await callback_query.answer()
    await States.settings_from.set()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
