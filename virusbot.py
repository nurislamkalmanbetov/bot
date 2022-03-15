from distutils  import command
import COVID19Py
import telebot
from telebot import types

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot('5272651894:AAECIUa0jAZ9-2bJwDq--Fv80SBPPrEtSFw')


@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton('Сша')
	btn2 = types.KeyboardButton('Киргизия')
	btn3 = types.KeyboardButton('Казакстан')
	btn4 = types.KeyboardButton('Россия')
	btn5 = types.KeyboardButton('Во всем мире')
	markup.add(btn1, btn2, btn3, btn4, btn5)

	send_mess = f'<b>Привет {message.from_user.first_name}!</b>\nВедите страну'
	bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):
	final_message = ''
	get_message_bot = message.text.strip().lower()
	if get_message_bot.lower() == 'сша':
		location = covid19.getLocationByCountryCode('US')
	elif get_message_bot.lower() == 'киргизия':
		location = covid19.getLocationByCountryCode('KG')
	elif get_message_bot.lower() == 'россия':
		location = covid19.getLocationByCountryCode('Ru')
	elif get_message_bot.lower() == 'казакстан':
		location = covid19.getLocationByCountryCode('KZ')
	else:
		location = covid19.getLatest()
		final_message = f"<u>Данные по всему миру:</u>\n<b>Заболевших: </b>{location['confirmed']:,}\n<b>Сметрей: </b>{location['deaths']:,}"

	if final_message == "":
		date = location[0]['last_updated'].split("T")
		time = date[1].split(".")
		final_message = f"<u>Данные по стране:</u>\nНаселение: {location[0]['country_population']:,}\n" \
				        f"Последнее обновление: {date[0]} {time[0]}\nПоследние данные:\n<b>" \
				        f"Заболевших: </b>{location[0]['latest']['confirmed']:,}\n<b>Сметрей: </b>" \
				        f"{location[0]['latest']['deaths']:,}"

	bot.send_message(message.chat.id, final_message, parse_mode='html')

bot.polling(none_stop=True)
