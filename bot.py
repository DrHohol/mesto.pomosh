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
    #user = Controller.user_exist()
    async with state.proxy() as data:
        data['name'] = message.text
        data['uid'] = message.from_user.id
    await message.answer("Тепер призвище:")
    await States.set_surname.set()


@dp.message_handler(state=States.set_surname)
async def choose_role(message: types.Message, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
        data['surname'] = message.text
    await States.set_number.set()
    await message.answer("Додайте ваш номер телефону. У форматi +380")


@dp.message_handler(state=States.set_number)
async def choose_role(message: types.Message, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await States.set_number.set()
    await message.answer(f"""
Вашi даннi:
Iм'я: {data['name']}
Призвище: {data['surname']}
Номер телефону: {data['phone_number']}""",
                         reply_markup=Keyboard.role_menu)
    controller.edit_user(controller.get_or_create_user(data['uid'])[0],
                         {'name': data['name'], 'surname': data['surname'], 'phone_number': data['phone_number']})
    await state.finish()
""" For driver """


@dp.message_handler(Text(equals="Водій"))
async def set_driver_menu(message: types.Message, state: FSMContext):
    await message.answer("Добре! Що ви хочете зробити?", reply_markup=Keyboard.menu('Водій'))


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
    await callback_query.message.edit_text("Добре, тепер куди",
                                           reply_markup=Buttons.select_region())
    await callback_query.answer()
    await States.to_drive.set()


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
    await message.answer(f"""Поїздка запланована на:{data['date']}
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
    await state.finish()


@dp.message_handler(Text(equals="Мої поїздки"))
async def my_drives(message: types.Message, state: FSMContext):
    user = controller.get_or_create_user(message.from_user.id)[0]
    print(user.id)
    drives = controller.get_drive_by({Drive.driver_id: user.id})
    pass_drives = controller.get_or_create_user(message.from_user.id)[0].drive
    for drive in drives:
        await message.answer(generate_info(drive),
                             reply_markup=Buttons.edit_drive_button(drive.id))
    for drives in pass_drives:
        await message.answer(generate_info(drive),
                             reply_markup=Buttons.cancel_passenger_button(drive.id))
    del drives
    del pass_drives
    #drives = Controller.get_drives


@dp.callback_query_handler(Text(startswith="del"), state="*")
async def delete_drive(callback_query: types.CallbackQuery, state: FSMContext):
    drive_id = callback_query.data.split('_')[1]
    # controller.delete_drive(drive_id)
    await callback_query.answer()


@dp.callback_query_handler(Text(startswith="edit"), state="*")
async def edit_drive(callback_query: types.CallbackQuery, state: FSMContext):
    drive_id = callback_query.data.split('_')[1]
    await callback_query.message.answer('Що ви хочете змiнити?',
                                        reply_markup=Buttons.edit_menu)
    await callback_query.answer()

'''For user'''


@dp.message_handler(Text(equals="Пасажир"), state="*")
async def passenger_menu(message: types.Message):
    await message.answer("Щас надо будет выбрать город из которого\
 хотите уехать, а потом куда. Поменять потом в настройках",
                         reply_markup=Keyboard.menu("Пасажир"))
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
            print(drive.place_from)


@dp.callback_query_handler(state=States.settings_from)
async def choose_role(callback_query: types.CallbackQuery, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
        data['drive_from'] = callback_query.data
    await callback_query.message.edit_text("Добре, тепер куди вам треба",
                                           reply_markup=Buttons.select_region(any=True))
    await callback_query.answer()
    await States.settings_to.set()


@dp.callback_query_handler(state=States.settings_to)
async def choose_role(callback_query: types.CallbackQuery, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
        data['drive_to'] = callback_query.data
    await callback_query.answer()
    await callback_query.message.edit_text("Скiльки людей",
                                           reply_markup=None)
    await States.settings_pass.set()


@dp.message_handler(state=States.settings_pass)
async def set_date(message: types.Message, state: FSMContext):

    async with state.proxy() as data:
        controller.edit_user(
            controller.get_or_create_user(message.from_user.id)[0],
            {'place_from': Buttons.regions[int(data['drive_from'])],
             'place_to': Buttons.regions[int(data['drive_to'])],
             'num_of_passengers': int(message.text)})

    await message.answer("Инфо есть. ща подборка")
    await state.finish()
    drives = controller.get_drive_by({
        Drive.place_from: data['drive_from'],
        Drive.place_to: data['drive_to']},
        places=int(message.text))
    for drive in drives:
        print(drive.place_from)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
