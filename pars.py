import requests
from bs4 import BeautifulSoup
import re

# Глобальные переменные для возможности работы с несколькими функциями.
# Global variables to work with some functions.
soup = None
ready_items = {}
# Эта переменная для текущего наименовния блюда, чтобы пользоваться пагинацией по текущему результату поиска.
#This variable for the current name of the dish is to use pagination according to the current search result.
current_search = None

# В соответствии с условиями формируем URL и делаем запрос, если запрос успешный - вытаскиваем html-ответ.
# In accordance with the conditions we form a URL and make a request, if the request is successful we pull out the HTML set.
def get_html(txt):
    global current_search
    full_url = None
    if 'https://' in txt:
        full_url = txt
    elif txt in '12345':
        full_url = 'https://povar.ru/xmlsearch?query=' + current_search + '&page=' + txt 
    else:
        full_url = 'https://povar.ru/xmlsearch?query=' + txt
    response = requests.get(full_url)
    if response.status_code == 200:  
        return get_soup(response.text)
    else:
        response_error = response.status_code 
        return response_error
    
# Конвертируем html в lxml для более быстрого поиска и готовим наш "глобальный суп".
# We convert HTML in LXML for a faster search and prepare our "global soup".
def get_soup(html):
    global soup
    soup = BeautifulSoup(html, "lxml")
    return soup

# Из нашего "супа" выбираем нужный текст, url-ки через тэги и атрибуты типа "class", "listRecipieTitle" и т.п.   
# Парсим название блюда и формируем ссылки на рецепт, добавляя всё в словарь.
# Словарь формируется в виде ключ - номер рецепта, значение - список название рецепта, ссылка.
# Нумерация рецептов будет использована для callback_data в InlineKeyboardButton кнопках.
# From our "soup" select the desired text.
# Parse the name of the dish and form links to the recipe, adding everything to the dictionary.
# The dictionary is formed in the form of the key: the recipe number, value: the list of the name recipe and link.
# The numbers of recipe be using for a callback data in inline keyboard button.
def get_links():
   global ready_items
   ready_items = {}
   for num, link in enumerate(soup.find_all('a', {'class': 'listRecipieTitle'})):
       ready_link = 'https://povar.ru'+link['href']
       name_recipe = link.get_text()
       ready_items[str(num)] = [name_recipe, ready_link]   
   return ready_items

# Проверяем статус нашего поиска.
# Function of check search status.
def search_status():
    check = soup.find('div', {'class': 'cat_sect_h'}).get_text()
    if 'Результаты поиска' in check:
        status = 'ok'
        return status
    elif 'Ничего не' in check:
        status = 'not found'
        return status

# Парсим ссылки на фото блюд.
# Parse the photo of the dish.
def get_photo_links():
    photo_links = [img_link.find('img').get('src') for img_link in soup.find_all('span', {'class': 'a thumb hashString'})]
    return photo_links

# Парсим полное описание рецепта.
# Parse a full description of recipe.
def get_detailed_recipe():
    ingredients = []
    for row in soup.find_all('li', {'itemprop': 'recipeIngredient'}):
        first_step = row.get_text().replace(u'\xa0', u' ')
        clear_row = re.sub(' +', ' ', first_step)
        ingredients.append(clear_row)
    for row_new in soup.find_all('div', {'class': 'detailed_step_description_big'}):    
        second_step = row_new.get_text()
        ingredients.append(second_step)
    full_text = '\n'.join(ingredients) 
    return full_text