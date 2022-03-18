from datetime import datetime

def generate_info(drive):

	text = f"""
📍Маршрут: {drive.place_from} → {drive.place_to}
🕒 Дата та час: {drive.departure_time.strftime("%d.%m.%y %H:%M")}
👫 Загальна кількість місць:  {drive.max_passengers_amount}
📞 Спосiб зв’язку: {drive.driver.contact_info}
📢 Важлива інформація: {drive.comment}"""
	
	return text