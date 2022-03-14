from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv
from keyboards import Buttons
from states import States
from controller import Controller
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
Номер телефону: {data['number']}""")
    Controller.get_or_create_user(data['uid']
                                  data['name'], data['surname'], data['phone_number'])
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
