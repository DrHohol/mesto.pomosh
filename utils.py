from datetime import datetime


def generate_info(drive):
	if drive.departure_time:
	    text = f"""
	📍 Маршрут: {drive.place_from} → {drive.place_to}
	🕒 Дата та час: {drive.departure_time.strftime("%d.%m.%y %H:%M")}
	👫 Загальна кількість місць:  {drive.max_passengers_amount}
	📞 Спосiб зв’язку: {drive.driver.contact_info}
	📢 Важлива інформація: {drive.comment}"""
	else:
		text = f"""
	📍 Маршрут: {drive.place_from} → {drive.place_to}
	⚠️ Регулярно: Так
	👫 Загальна кількість місць:  {drive.max_passengers_amount}
	📞 Спосiб зв’язку: {drive.driver.contact_info}
	📢 Важлива інформація: {drive.comment}"""

	return text

#If anyone is reading this now, know this:
#I didn't want to write crappy code, I had to...
