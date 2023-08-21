import os
import telebot
from telebot import types
import uuid
import time
import threading

# Замените YOUR_BOT_TOKEN на ваш токен бота
TOKEN = ''
bot = telebot.TeleBot(TOKEN)

# Путь к папке с разделами и подразделами
BASE_DIR = r'D:\Natlex praktika\bot_natlex'

# Словарь для хранения данных о путях кнопок
data_dict = {}



#### Тестирование очистки словаря индексов
def test_dict():
    global data_dict
    while True:
        print(data_dict.keys())
        
        time.sleep(3)  # Обновление каждые 5 минут



"""
Генерация уникального идентификатора
"""
def generate_uuid():
    return str(uuid.uuid4())


"""
Функция создания кнопок
"""
# Функция создания кнопок
def create_keyboard(directory, path):
    keyboard = types.InlineKeyboardMarkup()
    for item in directory:
        item_path = os.path.join(path, item) # Путь до item

        button_id = generate_uuid() 
        data_dict[button_id] = item_path
        
        button = types.InlineKeyboardButton(text=item, callback_data=button_id)
        keyboard.add(button)
    return keyboard




"""
Функция для обработки команды /start
"""
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=markup)
    show_sections(message.chat.id, BASE_DIR)




def search_files(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and not f.endswith('.py') and not f.endswith('.json')]

    return dirs, files



"""
Функция для отображения разделов и подразделов
"""
def show_sections(chat_id, path, message_id=None):
    dirs, files = search_files(path)

    # Если список не пуст, т.е. есть файлы с текстом
    if files:
        for file in files:
            with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
                description = f.read()
            
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=description)
    else:
        keyboard = create_keyboard(dirs, path)
        if message_id == None:
            bot.send_message(chat_id, "Выберите раздел или подраздел:", reply_markup=keyboard)
        else:
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=keyboard)
        # bot.send_message(chat_id, "Выберите раздел или подраздел:", reply_markup=keyboard)




"""
Функция для обработки коллбэков кнопок
"""
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.message:
        button_id = call.data
        item_path = data_dict.get(button_id)

        if item_path:
            show_sections(call.message.chat.id, item_path, call.message.message_id)
            data_dict.pop(button_id, None)



if __name__ == "__main__":
    # Запуск потока для периодического обновления
    update_thread = threading.Thread(target=test_dict)
    update_thread.daemon = True  # Поток будет остановлен при завершении основного потока
    update_thread.start()
    bot.polling(none_stop=True)

