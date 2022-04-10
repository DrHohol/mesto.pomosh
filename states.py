from aiogram.dispatcher.filters.state import State, StatesGroup


class States(StatesGroup):
	choose_role = State()
	set_name = State()
	set_surname = State()
	set_number = State()
	user_from = State()
	user_to = State()
	from_drive = State()
	to_drive = State()
	date = State()
	time = State()
	max_pass = State()
	comment = State()
	settings_from = State()
	settings_to = State()
	settings_pass = State()
	admin = State()