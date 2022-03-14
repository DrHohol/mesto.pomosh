from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
	choose_role = State()
	set_name = State()
	set_surname = State()
	set_number = State()
	user_from = State()
	user_to = State()