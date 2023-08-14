import telebot
from telebot import types
import json
import time
import threading




"""
Функция загрузки токена
"""
def load_token(file_path):
    with open(file_path, 'r') as file:
        token = file.read().strip()
    return token




ALLOWED_USERNAMES = []
TOKEN = load_token('token.txt')
fes= 2

bot = telebot.TeleBot(TOKEN)




"""
Функци загрузки файла конфигурации
"""
def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config




"""
Функция чтения списка ALLOWED_USERNAMES каждые 5 минут, создает новый поток
"""
def update_allowed_usernames():
    global ALLOWED_USERNAMES
    while True:
        new_allowed_usernames_data = load_config('allowed_usernames.json')
        new_allowed_usernames = [user['username'] for user in new_allowed_usernames_data]
        if new_allowed_usernames != ALLOWED_USERNAMES:
            ALLOWED_USERNAMES = new_allowed_usernames
            print("Allowed usernames updated:", ALLOWED_USERNAMES)
        
        time.sleep(300)  # Обновление каждые 5 минут
        



"""
Фильтр доступа по username
"""
@bot.message_handler(func=lambda message: message.from_user.username not in ALLOWED_USERNAMES)
def some(message):
   bot.send_message(message.chat.id, "Прости, нет доступа")




"""
Создание кнопок по файлу конфигурации
"""
def create_keyboard(config, section_title=None):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    # Если нет заголовка, то мы создаем главные кнопки по файлу конфигурации
    if section_title == None:
        for section in config:
            button = types.InlineKeyboardButton(text=section['title'], callback_data=section['title'])
            keyboard.add(button)
    
    # Если задан заголовок, значит ищем подразделы
    else:
        for section in config:
            if section_title and section['title'] == section_title:
                for subsection in section.get('subsections', []):
                    button = types.InlineKeyboardButton(text=subsection['title'], callback_data=subsection['title'])
                    keyboard.add(button)
                break

    return keyboard




"""
Основное меню    
"""
def main_menu(id, text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Главное меню')

    markup.add(item1)
    bot.send_message(id, text, reply_markup=markup)




"""
Перехватчик start
"""
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем стартовое меню и пишем приветсвенное сообщение
    hello_message = f"Привет, {message.from_user.first_name}!"        
    main_menu(message.chat.id, hello_message)
    bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=create_keyboard(config))




"""
Перехватчик и метод получения текстовых сообщений
"""
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.type == 'private': # Если личное сообщение, а не канал какой-то
        if message.text == "Главное меню":
            main_menu(message.chat.id, "Главное меню")  
            bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=create_keyboard(config))


"""
Перехватчик результатов кнопок
"""
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.message:
        for section in config:
            if call.data == section['title']:
                description = section.get('description', '')
                subsections = section.get('subsections', [])
                # Если описание не пустое, то выводи описание
                if description != '':
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=description)

                # Если есть подразделы, то меняем кнопки
                if subsections != None:
                    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_keyboard(config, section['title']))
                break
            # Если это подраздел, то ищем среди них нужное title и выводим desctiption
            else:
                for subsection in section.get('subsections', []):
                    if call.data == subsection['title']:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=subsection['description'])
                        break
                





if __name__ == '__main__':
    config = load_config('config.json')
    # Запуск потока для периодического обновления
    update_thread = threading.Thread(target=update_allowed_usernames)
    update_thread.daemon = True  # Поток будет остановлен при завершении основного потока
    update_thread.start()


    bot.polling(none_stop=True, interval=0)
