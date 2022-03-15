from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv
from keyboards import Buttons, Keyboard
from states import States
#from controller import Controller
from datetime import datetime
import os

load_dotenv()

bot = Bot(token=os.environ.get("TOKEN"))
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=["help", "start"], state="*")
async def hello(message: types.Message):
    await message.answer(
        "Привiт! Цей бот допоможе вам евакуюватись до безпечного мiсця")
    await message.answer("Щоб продовжити введiть iнформацiю про себе. Почнемо з iм'я:")
    await States.set_name.set()


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
    print(message)
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
        data['number'] = message.text
    await States.set_number.set()
    await message.answer(f"""
Вашi даннi:
Iм'я: {data['name']}
Призвище: {data['surname']}
Номер телефону: {data['number']}""",
reply_markup=Keyboard.role_menu)
    #Controller.get_or_create_user(data['uid']
   #                               data['name'], data['surname'], data['phone_number'],
   #                               reply_markup = Keyboard.role_menu)
    await state.finish()
""" For driver """
@dp.message_handler(Text(equals="Водій"))
async def set_driver_menu(message : types.Message, state: FSMContext):
    await message.answer("Добре! Що ви хочете зробити?",reply_markup=Keyboard.driver_menu)

@dp.message_handler(Text(equals="Додати оголошення"),state="*")
async def set_driver_menu(message : types.Message, state: FSMContext):
    await message.answer("Какой-то биг текст с уточнениями. Выберите начальный пункт",
        reply_markup=Buttons.select_region())
    await States.from_drive.set()

@dp.callback_query_handler(state=States.from_drive)
async def choose_role(callback_query: types.CallbackQuery, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
                data['drive_from'] = callback_query.data
    await callback_query.message.edit_text("Добре, тепер куди",
        reply_markup = Buttons.select_region())
    await callback_query.answer()
    await States.to_drive.set()

@dp.callback_query_handler(state=States.to_drive)
async def choose_role(callback_query: types.CallbackQuery, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
                data['drive_to'] = callback_query.data
    await callback_query.message.answer("Тепер вкажiть дату у\
форматi ДД.ММ.РР ГГ:ХХ")
    await callback_query.answer()
    await States.date.set()

@dp.message_handler(state=States.date)
async def set_driver_menu(message : types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['date'] = datetime.strptime(message.text, "%d.%m.%y %H:%M")
        except Exception as e:
            print(e)
            await message.answer(f"Wrong format")
            print(data['date'])
    await message.answer(f"""Поiздка запланована на:{data['date']}
Початковый пункт: {Buttons.regions[int(data['drive_from'])]}
Кiнечний пункт: {Buttons.regions[int(data['drive_to'])]}""")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
