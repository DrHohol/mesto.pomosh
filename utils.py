from datetime import datetime


def generate_info(drive,driver):
	if drive.departure_time:
		r = '🕒 Дата та час: {drive.departure_time.strftime("%d.%m.%y %H:%M")}'

	else:
		r = "⚠️ Регулярно: Так"
	text = f"""
📍 Маршрут: {drive.place_from} → {drive.place_to}
{r}
👫 Загальна кількість місць:  {drive.max_passengers_amount}
📞 Спосiб зв’язку: {driver.contact_info}
📢 Важлива інформація: {drive.comment}"""

	return text

#If anyone is reading this now, know this:
#I didn't want to write crappy code, I had to...
