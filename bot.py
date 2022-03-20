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
    controller.get_or_create_user(message.from_user.id)
    await message.answer("""
Привіт 👋
Я бот "Місце допомоги"
Мої творці просять вас допомагати одне одному, по можливості, на безкоштовній основі. Разом ми переможемо 💪🇺🇦

Я знаходжу людей, які можуть допомогти з евакуацією, або тих, хто шукає спосіб евакуюватися 🙏

❗️ Будьте пильні та перевіряйте водіїв перед узгодженням поїздки ❗️""")

    await message.answer("Що вам потрібно: шукаю допомогу / можу допомогти 👇",
                         reply_markup=Keyboard.role_menu)


@dp.message_handler(Text(equals="Мої поїздки"), state='*')
async def my_drives(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.finish()
    user = controller.get_or_create_user(message.from_user.id)[0]
    drives = controller.get_drive_by({Drive.driver_id: user.id})
    if not drives:
        await message.answer("""
            Зараз у вас немає жодної поїздки. Натисність кнопку "Додати оголошення" щоб залишити поїздку 👇""",
                             reply_markup=Keyboard.menu("Я Водій"))
    for drive in drives:
        await message.answer(generate_info(drive),
                             reply_markup=Buttons.edit_drive_button(drive.id))
    del drives
    #drives = Controller.get_drives


@dp.message_handler(state=States.set_name)
async def choose_role(message: types.Message, state: FSMContext):
    user = controller.get_or_create_user(
        message.from_user.id)[0]

    if not user.contact_info:
        async with state.proxy() as data:
            data['name'] = message.text
            data['uid'] = message.from_user.id
        await States.set_number.set()
        await message.answer("📞 Як з вами можна зв’язатись?")
    else:
        await message.answer('Інформацію оновлено.')
        controller.edit_user(user,
                             {'name': message.text})
        await state.finish()


@dp.message_handler(state=States.set_number)
async def choose_role(message: types.Message, state: FSMContext):
    #user = Controller.user_exist()
    async with state.proxy() as data:
        data['phone_number'] = message.text
    if data.get('editing'):
        controller.edit_user(
            controller.get_or_create_user(message.from_user.id)[0],
            {'contact_info': message.text})
        await state.finish()
        await message.answer("інформацію оновлено.",
                             reply_markup=Keyboard.menu('Я Водій'))
    else:
        await message.answer(f"""
    Ваші данні:
    Ім'я: {data['name']}
    Спосіб зв'язку: {data['phone_number']}""",
                             reply_markup=Keyboard.menu('Я Водій'))
        controller.edit_user(controller.get_or_create_user(data['uid'])[0],
                             {'name': data['name'], 'contact_info': data['phone_number']})
        await state.finish()
""" For driver """


@dp.message_handler(Text(equals="Надати допомогу"), state='*')
async def set_driver_menu(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.finish()
    if not controller.get_or_create_user(message.from_user.id)[0].name:
        await message.answer("Щоб продовжити введіть інформацію про себе. Почнемо з ім'я:")
        await States.set_name.set()
    else:
        await message.answer("Добре! Що ви хочете зробити?", reply_markup=Keyboard.menu('Я Водій'))


@dp.message_handler(Text(equals="Додати оголошення"), state="*")
async def set_driver_menu(message: types.Message, state: FSMContext):
    await message.answer("""
📍 Оберіть місто, з якого ви будете виїжджати, щоб люди поруч змогли вас знайти

Якщо у списку не має вашого міста, виберіть обласний центр 👇""",
                         reply_markup=Buttons.select_region())
    await States.from_drive.set()


@dp.callback_query_handler(state=States.from_drive)
async def choose_role(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data.startswith("page_"):
        page = callback_query.data.split("_")[1]
        await callback_query.message.edit_reply_markup(Buttons.select_region(
            nowhere=False, page=int(page)))
    else:
        async with state.proxy() as data:
            data['drive_from'] = callback_query.data
        await States.to_drive.set()
        await callback_query.message.edit_text("""
📍 Оберіть напрям, куди ви плануєте поїхати

Якщо у списку немає бажаного міста, виберіть обласний центр. Точне місто ви зможете вказати пізніше 👇""",
                                               reply_markup=Buttons.select_region(nowhere=True))
        await callback_query.answer()


@dp.callback_query_handler(state=States.to_drive)
async def choose_role(callback_query: types.CallbackQuery, state: FSMContext):
    #user = Controller.user_exist()
    if callback_query.data.startswith("page_"):
        page = callback_query.data.split("_")[1]
        await callback_query.message.edit_reply_markup(Buttons.select_region(
            nowhere=True, page=int(page)))
    else:
        async with state.proxy() as data:
            if data.get('editing'):
                controller.edit_drive(
                    data['current_drive'],
                    {'place_from': Buttons.regions_from[int(data['drive_from'])],
                     'place_to': Buttons.regions_to[int(callback_query.data)]})
                await callback_query.message.edit_text(
                    "Маршрут змінений", reply_markup=None)
                await state.finish()
            else:
                data['drive_to'] = callback_query.data
                await callback_query.message.answer("👫 Введіть цифрою кількість пасажирів, яких ви можете взяти з собою 👇")
                await callback_query.answer()
                await States.max_pass.set()


@dp.message_handler(state=States.max_pass)
async def set_driver_menu(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.isdigit() and int(message.text) >= 1:
            if data.get('editing'):
                controller.edit_drive(
                    data['current_drive'],
                    {'max_passengers_amount': int(message.text)})
                await message.answer('Готово',
                    reply_markup=Keyboard.menu('Я Водій'))
                await state.finish()
            else:
                data['max_pass'] = int(message.text)
                await message.answer("""📣 Важлива інформація

Залиште будь-яку важливу інформацію на вашу думку:

Наприкад:
- ваше ім’я
- назва населеного пункту або міста, звідки ви будете виїжджати 📍
- чи можна з тваринами 🐶
- кількість багажу на одну особу 🧳
- вартість поїздки 💰
- будь-яку іншу інформацію
""", reply_markup=Keyboard.skip)
                await States.comment.set()
        else:
            await message.answer("Помилка. Можна лише 1 або більше.")


@dp.message_handler(state=States.comment)
async def set_date(message: types.Message, state: FSMContext):
    if message.text == "Пропустити":
        message.text = "Відсутня"
    async with state.proxy() as data:
        if data.get('editing'):
            controller.edit_drive(
                data['current_drive'],
                {'comment': message.text})
            await message.answer('Коментар оновлено')
            await state.finish()
        else:
            data['comment'] = message.text
            await message.answer("""
🕒 Дата та час

Напишіть дату та час, о котрій ви будете виїжджати, за прикладом, наведеним нижче.

Дата та час: 20.03.2022 14:30""")
            await States.date.set()


@dp.message_handler(state=States.date)
async def add_drive(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['date'] = datetime.strptime(message.text, "%d.%m.%y %H:%M")
            if data['date'] < datetime.now():
                raise ValueError
            if data.get('editing'):
                controller.edit_drive(data['current_drive'],
                                      attrs={'departure_time': data['date']})
                await message.answer(f'Дата змінена. Нова дата: {data["date"]}')
                await state.finish()
                del data['editing']
            else:
                drive = controller.create_drive(Buttons.regions_from[int(data['drive_from'])],
                                                Buttons.regions_to[int(
                                                    data['drive_to'])],
                                                message.from_user.id,
                                                data['max_pass'],
                                                data['date'],
                                                data['comment'])
                await message.answer(f"""
✅ Ваша пропозиція поїздки створена 

📍 Маршрут: {drive.place_from} → {drive.place_to}
🕒 Дата та час: {drive.departure_time.strftime("%d.%m.%y %H:%M")}
👫 Загальна кількість місць: {drive.max_passengers_amount}
📞 Спосіб зв’язку: {drive.driver.contact_info}
📢 Важлива інформація: {drive.comment}

Дякуємо вам 🙏""",
                                     reply_markup=Keyboard.menu('Я Водій'))
                await send_notify(drive)
                await state.finish()
        except Exception as e:
            print(e)
            await message.answer(f"Упс, ви не вірно ввели дату. Спробуйте знову і запишіть дату та час згідно прикладу 👇")


async def send_notify(drive):
    users = controller.get_user_by(
        drive.place_from,
        drive.place_to,
        drive.max_passengers_amount)
    print(users)
    if users:
        for user in users:
            await bot.send_message(
                user.chat_id,
                text=f"""
✅ Знайдена нова поїздка для вас
📍 Маршрут: {drive.place_from} → {drive.place_to}
🕒 Дата та час: {drive.departure_time.strftime("%d.%m.%y %H:%M")}
👫 Загальна кількість місць: {drive.max_passengers_amount}
📞 Спосіб зв’язку: {drive.driver.contact_info}
📢 Важлива інформація: {drive.comment}""")
    # print(users[0].name)


@dp.callback_query_handler(Text(startswith="del"), state="*")
async def delete_drive(callback_query: types.CallbackQuery, state: FSMContext):
    drive_id = callback_query.data.split('_')[1]
    controller.delete_drive(controller.get_drive_by(
        {Drive.id: drive_id})[0])
    await callback_query.message.delete()
    await bot.send_message(callback_query.from_user.id,
                           "Видалено", reply_markup=Keyboard.menu("Я Водій"))
    await callback_query.answer()


@dp.callback_query_handler(Text(startswith="edit"), state="*")
async def edit_drive(callback_query: types.CallbackQuery, state: FSMContext):
    drive_id = callback_query.data.split('_')[1]
    async with state.proxy() as data:
        data['current_drive'] = drive_id
        data['editing'] = True
    await callback_query.message.answer('Що ви хочете змінити?',
                                        reply_markup=Buttons.edit_menu)
    await callback_query.answer()


@dp.callback_query_handler(Text(equals='date_edit'))
async def edit_date(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Вкажіть дату у\
форматі ДД.ММ.РР ГГ:ХХ")
    await States.date.set()


@dp.callback_query_handler(Text(equals='route'), state="*")
async def edit_date(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Звідки прямуєте",
                                           reply_markup=Buttons.select_region(nowhere=False))
    await States.from_drive.set()


@dp.callback_query_handler(Text(equals='com_edit'), state="*")
async def edit_date(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Коментар")
    await States.comment.set()


@dp.callback_query_handler(Text(equals='pass_count'), state="*")
async def edit_pass_count(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Кількість пасажирів")
    await States.max_pass.set()

'''For user'''


@dp.message_handler(Text(equals="Шукати допомогу"), state="*")
async def passenger_menu(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.finish()
    await message.answer("""
⚠️ НЕ НАДСИЛАЙТЕ ПЕРЕДОПЛАТУ ⚠️
Пам’ятайте, майже усі перевізники беруть кошти після завершення поїздки готівкою 🇺🇦💰""",
                         reply_markup=Keyboard.menu("Я Пасажир"))
    user = controller.get_or_create_user(message.from_user.id)[0]
    if not user.place_from:
        await message.answer("""
📍 Оберіть місто, з якого ви будете виїжджати, щоб люди поруч змогли вас знайти

Якщо у списку не має вашого міста, виберіть обласний центр 👇
""",
                             reply_markup=Buttons.select_region())
        await States.settings_from.set()
    else:

        drives = controller.get_drive_by({
            Drive.place_from: user.place_from,
            Drive.place_to: user.place_to},
            places=user.num_of_passengers)
        if not drives:
            await message.answer("""
Нажаль, зараз немає поїздок за вашим напрямом 😔

Вам потрібно перейти у розділ «Змінити маршрут» та змінити напрям вашої поїздки 👇

""", reply_markup=Keyboard.menu("Я Пасажир"))
        else:
            for drive in drives:
                await message.answer(
                    generate_info(drive),
                    reply_markup=Keyboard.menu('Я Пасажир'))


@dp.callback_query_handler(state=States.settings_from)
async def set_start(callback_query: types.CallbackQuery, state: FSMContext):
    #user = Controller.user_exist()
    if callback_query.data.startswith("page_"):
        page = callback_query.data.split("_")[1]
        await callback_query.message.edit_reply_markup(Buttons.select_region(
            nowhere=False, page=int(page)))
    elif callback_query.data.isdigit():
        async with state.proxy() as data:
            data['drive_from'] = callback_query.data
        await callback_query.message.edit_text("""
📍 Оберіть напрям, куди ви плануєте поїхати

Якщо у списку немає бажаного міста, виберіть обласний центр👇""",
                                               reply_markup=Buttons.select_region(nowhere=True))
        await callback_query.answer()
        await States.settings_to.set()
    else:
        await callback_query.answer()
        await States.settings_to.set()


@dp.callback_query_handler(state=States.settings_to)
async def set_finish(callback_query: types.CallbackQuery, state: FSMContext):

    await callback_query.answer()
    if callback_query.data.startswith("page_"):
        page = callback_query.data.split("_")[1]
        await callback_query.message.edit_reply_markup(Buttons.select_region(
            nowhere=False, page=int(page)))

    elif callback_query.data.isdigit():
        async with state.proxy() as data:
            data['drive_to'] = callback_query.data

        user = controller.get_or_create_user(
            callback_query.from_user.id)[0]
        if user.num_of_passengers:
            controller.edit_user(user,
                                 {'place_from': Buttons.regions_from[int(data['drive_from'])],
                                  'place_to': Buttons.regions_to[int(callback_query.data)]})
            await callback_query.message.edit_text("Оновлено!",
                                                   reply_markup=Buttons.find)
            await state.finish()

        else:
            await callback_query.message.edit_text("👫 Скільки місць в авто вам потрібно? 👇",
                                                   reply_markup=None)
            await States.settings_pass.set()
    else:
        await callback_query.answer()
        await state.finish()


@dp.message_handler(state=States.settings_pass)
async def get_drives(message: types.Message, state: FSMContext):

    user = controller.get_or_create_user(message.from_user.id)[0]

    passengers = message.text
    if passengers.isdigit() and int(passengers) >= 1:
        if user.place_from:
            controller.edit_user(user,
                                 {'num_of_passengers': int(message.text)})
            await message.answer("Інформацію оновлено. Показати оголошення?",
                                 reply_markup=Buttons.find)
            await state.finish()
        else:
            async with state.proxy() as data:
                controller.edit_user(user,
                                     {'place_from': Buttons.regions_from[int(data['drive_from'])],
                                      'place_to': Buttons.regions_to[int(data['drive_to'])],
                                      'num_of_passengers': int(message.text)})

            await message.answer("Інфомація присутня.")
            await state.finish()
            drives = controller.get_drive_by({
                Drive.place_from: Buttons.regions_from[int(data['drive_from'])],
                Drive.place_to: Buttons.regions_to[int(data['drive_to'])]},
                places=int(message.text))
            for drive in drives:
                await message.answer(
                    generate_info(drive),
                    reply_markup=Keyboard.menu('Я Пасажир'))
    else:
        await message.answer("Невірний формат. Введіть будь ласка цифру, більшу за 0")


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
            """Нажаль, зараз немає поїздок за вашим напрямом 😔

Вам потрібно перейти у розділ «Налаштування» та змінити напрям вашої поїздки👇""")
    for drive in drives:
        if drive.departure_time > datetime.now():
            await bot.send_message(
                callback_query.from_user.id,
                generate_info(drive),
                reply_markup=Keyboard.menu('Я Пасажир'))


@dp.message_handler(lambda message: message.text in ["Змінити маршрут","Редагувати поїздки"], state="*")
async def settings(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.finish()
    await message.answer("Що ви хочете змінити?",
                         reply_markup=Buttons.edit_data_menu)


@dp.message_handler(Text(equals="Вимкнути повідомлення"), state="*")
async def notify(message: types.Message, state: FSMContext):
    if await state.get_state():
        await state.finish()
    user = controller.get_or_create_user(message.from_user.id)[0]
    if user.active_search:
        controller.edit_user(user,
                             {'active_search': False})
        await message.answer("Ваші повідомлення вимкнуті",
                             reply_markup=Keyboard.menu("Я Пасажир"))
    else:
        controller.edit_user(user,
                             {'active_search': True})
        await message.answer("Ваші повідомлення увімкнені",
                             reply_markup=Keyboard.menu("Я Пасажир"))


""" Editing user info """


@dp.callback_query_handler(Text(equals='nm_chng'), state="*")
async def change_name(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введіть нове ім'я")
    await callback_query.answer()
    await States.set_name.set()


@dp.callback_query_handler(Text(equals='ph_chng'))
async def change_name(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['editing'] = True
    await callback_query.message.answer("Вкажіть спосіб зв'язку")
    await callback_query.answer()
    await States.set_number.set()


@dp.callback_query_handler(Text(equals='u_count'))
async def change_pass_count(callback_query: types.CallbackQuery):

    await callback_query.message.answer("Введіть вашу кількість")
    await callback_query.answer()
    await States.settings_pass.set()


@dp.callback_query_handler(Text(equals='u_from'))
async def change_route_pass(callback_query: types.CallbackQuery):

    await callback_query.message.answer("Оберіть точку виїзду",
                                        reply_markup=Buttons.select_region())
    await callback_query.answer()
    await States.settings_from.set()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)