from telebot import *
import pars
from utils.utilites import send_content, get_help_text, bot


task_switcher = True

@bot.message_handler(commands=['start'])
def ready_work(message):
	global task_switcher
	task_switcher = True
	bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAINMmHxQ--bU7k29ptmeMC9X6c8IuQOAAJmBAACR_sJDEKts0woFwdfIwQ')
	bot.send_message(message.chat.id, 'Привет! Я Бот Кулинар, помогу тебе в приготовлении вкусняшек.\nНапиши мне название блюда и погнали! 🥧')

@bot.message_handler(commands=['new_search'])
def refresh_search(message):
	global task_switcher
	task_switcher = True
	bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIjjGMSDDQJoyeNo2hN_jt5YkIQygmLAAJsBAACR_sJDHDW7bY87FWhKQQ')
	bot.send_message(message.chat.id, 'Давай поищем ещё рецепты!🍔')

@bot.message_handler(commands=['help'])
def refresh_search(message):
	global task_switcher
	task_switcher = True
	bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIjkGMSDE06Xt7juqwr5bWnAS-4GDH0AAJ7BAACR_sJDEp5b1zC0IaRKQQ')
	bot.send_message(message.chat.id, get_help_text())

@bot.message_handler(content_types=['text'])
def search_text(message):											 
	response_status = pars.get_html(message.text.lower())
	global task_switcher
	if response_status is not int:
		search_status = pars.search_status()
		if search_status == 'ok':
			if task_switcher and 'Начать новый поиск' not in message.text:
				pars.current_search = message.text.lower()
				menu_keyboard = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
				menu_button1 = types.KeyboardButton('1')
				menu_button2 = types.KeyboardButton('2')
				menu_button3 = types.KeyboardButton('3')
				menu_button4 = types.KeyboardButton('4')
				menu_button5 = types.KeyboardButton('5')
				menu_button_new_search = types.KeyboardButton('Начать новый поиск')
				menu_keyboard.row(menu_button1, menu_button2, menu_button3, menu_button4, menu_button5)
				menu_keyboard.row(menu_button_new_search)
				task_switcher = False
				bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAINNGHxRdAMX6j8BZdNWMN2shxoDYz1AAJqBAACR_sJDOMa1wrTzyP9IwQ')
				bot.send_message(message.chat.id, "А вот и рецептики!", reply_markup=menu_keyboard)
				send_content(message.chat.id)
			else:
				if message.text in '12345':
					send_content(message.chat.id)
				elif 'Начать новый поиск' in message.text:
					task_switcher = True
				else:
					bot.delete_message(message.chat.id, message.message_id)
		elif search_status == 'not found' and task_switcher:
			bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIjPGMNuKGoxFSmoRxzCIQ-_O7xgzIwAAJ-BAACR_sJDPdD7_9PHlkbKQQ')
			bot.send_message(message.chat.id, "Я ничего не нашёл. Попробуй ещё раз!")
		elif search_status == 'not found' and not task_switcher:
			bot.delete_message(message.chat.id, message.message_id)
	else:
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIiSmMHOAxoovzTafB5ir0VbyjTTctjAAKDBAACR_sJDG8VW4WhLqTWKQQ')
		bot.send_message(message.chat.id, "Ой! Что-то пошло не так, видимо сервер не отвечает.")



# Декоратор обработчика callback запросов с функцией, выдающая нам полный текст рецепта.
# Callback query handler deсorator with a function that gives us the full text of the recipe.
@bot.callback_query_handler(func=lambda call: True)
def callback_catcher(call):
	pars.get_html(pars.ready_items[call.data][1])
	recipe_text = pars.get_detailed_recipe()
	bot.send_message(call.message.chat.id, pars.ready_items[call.data][0] +' 👀')
	bot.send_message(call.message.chat.id, recipe_text)


if __name__ == "__main__":
	bot.infinity_polling()