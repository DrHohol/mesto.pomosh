def generate_info(drive):

	text = f"""Поїздка номер {drive.id}
Мiсць на момент додавання: {drive.max_passengers_amount}
Звiдки: {drive.place_from}
Куди: {drive.place_to}
Коли: {drive.departure_time}"""
	
	return text