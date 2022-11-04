from telebot import *
import pars
from conf import TOKEN_BOT

bot = telebot.TeleBot(TOKEN_BOT)

def get_help_text():
    help_txt = None
    with open(r'utils/help.txt', 'r', encoding='utf-8') as file:
        help_txt = file.read()
    return help_txt


# Функция отвечающая за выдачу результата поискового запроса.
# The function responsible for issuing the result of the search query.
def send_content(chat_id):
	find_links = pars.get_links()
	find_image = pars.get_photo_links()
	for num, item in enumerate(zip(find_links.values(), find_image)):
		keyboard = types.InlineKeyboardMarkup()
		recipe_button = types.InlineKeyboardButton(text="Посмотреть рецепт", callback_data=str(num))
		keyboard.add(recipe_button)
		bot.send_photo(chat_id, item[1], caption=item[0][0], protect_content=True, reply_markup=keyboard)
		bot.send_chat_action(chat_id, 'typing')