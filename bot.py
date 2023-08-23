import os
import telebot
from telebot import types
import time
import json




"""
Функция загрузки токена
"""
def load_token(file_path):
    with open(file_path, 'r') as file:
        token = file.read().strip()
    return token




# Запуск бота
TOKEN = load_token('TOKEN.txt')
bot = telebot.TeleBot(TOKEN)


# Получение текущего пути к файлу бота
bot_directory = os.path.dirname(os.path.abspath(__file__))

PATH_TO_DOCS = "docs"

# Путь к папке с разделами и подразделами
BASE_DIR = os.path.join(bot_directory, PATH_TO_DOCS)


ALLOWED_USERS = []
# USERS_INFO = {}



class UsersInfo:
    def __init__(self):
        self.__users_info = {}

    def get_user_info(self, user_id):
        return self.__users_info.get(user_id, None)

    def add_user_info(self, user_id, user_info):
        self.__users_info[user_id] = user_info

    """
    Обновление current_path пользователя
    """
    def update_user_path(self, user_id, new_path):
        user_info = self.get_user_info(user_id)
        if user_info:
            user_info["current_path"] = new_path

    """
    Откат current_path пользователя до BASE_DIR
    """
    def refresh_current_path(self, user_id):
        user_info = self.get_user_info(user_id)
        if user_info:
            user_info["current_path"] = BASE_DIR

    """
    Загрузка инофрмации о пользователе
    """
    def load_user_info(self, user_id, username):
        found_user = get_user_from_allowed_users(username) 
        found_user["current_path"] = BASE_DIR

        self.add_user_info(int(user_id), found_user)



# Создаем объект класса UsersInfo
USERS_INFO = UsersInfo()



"""
Класс опросов.
Создание опроса, сохранение, загрузка в json.
Отправка пользователю.
"""
class Survey:
    def __init__(self):
        self.__survey = {}
        self.date = ""
        self.name = ""
        self.users = []

    @property
    def survey(self):
        return self.__survey

    @survey.setter
    def survey(self, dict):
        self.__survey = dict.copy()
    
    def get_question(self):
        try:
            return self.survey["question"]
        except:
            print("Ошибка, нет вопроса в опросе")
            return "Вопрос"
    
    def get_options(self):
        try:
            return self.survey["options"]
        except:
            print("Ошибка, нет ответов в опросе")
            return ['1 ответ', '2 ответ', '3 ответ']
        
    def load_survey(self, path):
        #Получаем по пути json и читаем его
        # Заполняем в список survey
        None

    def save_survey(self, path, name):
        # Загружаем в json фалй
        None

    def send_survey(self, message):
        bot.send_poll(message.chat.id, question=self.get_question(), options=self.get_options())





survey = Survey()
survey.survey = {
    "question": "Какой ваш любимый цвет?",
    "options": ["Красный", "Синий", "Зеленый"],
}



#### Тестирование работы бота с выводом инфы
def test_bot():
    while True:
        time.sleep(3)  # Обновление каждые 5 минут




"""
Очистка бота
"""
def clear_bot():
    global USERS_INFO




"""
Функци загрузки json файла
"""
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        config = json.load(file)
    return config




"""
Получить пользователя по username из списка пользователей
"""
def get_user_from_allowed_users(username):
    found_user = None
    for user in ALLOWED_USERS:
        if user["username"] == username:
            found_user = user.copy()
            break

    return found_user
    



"""
Главное меню клавиатура
"""
def main_keyboard(id, text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Главное меню')

    markup.add(item1)
    bot.send_message(id, text, reply_markup=markup)




"""
Функция создания кнопок
"""
def create_keyboard(directory, path):
    keyboard = types.InlineKeyboardMarkup()
    for item in directory:
        button = types.InlineKeyboardButton(text=item, callback_data=item)
        keyboard.add(button)
    return keyboard




"""
Фильтр пользователей доступа к боту
"""
def user_allowed(func):
    def wrapper(message):
        user = get_user_from_allowed_users(message.from_user.username)
        if user:
            func(message)
        else:
            bot.send_message(message.chat.id, "Вы не имеете доступа к боту")
    return wrapper




"""
Функция для обработки команды /start
"""
@bot.message_handler(commands=['start'])
@user_allowed
def start(message):

    # Создаем стартовое меню и пишем приветсвенное сообщение
    hello_message = f"Привет, {message.from_user.first_name}!"        
    main_keyboard(message.chat.id, hello_message) 

    print(message.from_user.id)
    
    # Добавления пользователся в локальный словарь по user_id
    USERS_INFO.load_user_info(message.from_user.id, message.from_user.username)
    # load_user_info(message.from_user.id, message.from_user.username)

    USERS_INFO.refresh_current_path(message.from_user.id)
    # refresh_current_path(message.from_user.id)

    show_sections(message.chat.id, BASE_DIR)

    # survey.send_survey(message)



"""
Перехватчик и метод получения текстовых сообщений
"""
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.type == 'private': # Если личное сообщение, а не канал какой-то
        if message.text == "Главное меню":
            # main_keyboard(message.chat.id, "Главное меню")  
            USERS_INFO.refresh_current_path(message.from_user.id)
            # refresh_current_path(message.from_user.id)
            
            show_sections(message.chat.id, BASE_DIR)




"""
Поиск файлов по пути для отображения кнопок
"""
def search_files(path):
    dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d)) and d != "surveys"]
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and not f.endswith('.py') and not f.endswith('.json')]

    return dirs, files




"""
Функция для отображения разделов и подразделов
"""
def show_sections(chat_id, path, message=None):
    try:
        dirs, files = search_files(path)
    except:
        bot.send_message(chat_id, "Нет такого файла")
        USERS_INFO.refresh_current_path(message.chat.id)
        # refresh_current_path(message.chat.id)
        return

    # Если список не пуст, т.е. есть файлы с текстом
    if files:
        for file in files:
            with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
                description = f.read()
            
            bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=description)
            USERS_INFO.refresh_current_path(message.chat.id)
            # refresh_current_path(message.chat.id) # Очищаем путь, т.к. был выведен текст без кнопок
    else:
        keyboard = create_keyboard(dirs, path)
        if message == None:  
            bot.send_message(chat_id, "Выберите раздел:", reply_markup=keyboard)
        else:
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message.message_id, reply_markup=keyboard)




"""
Функция для обработки коллбэков кнопок
"""
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    # global USERS_INFO
    if call.message:
        data = call.data

        if data:
            new_path = os.path.join(USERS_INFO.get_user_info(call.from_user.id)["current_path"], data) # Путь до item
            USERS_INFO.update_user_path(call.from_user.id, new_path)
            # USERS_INFO[call.from_user.id]["current_path"] = \
            # os.path.join(USERS_INFO[call.from_user.id]["current_path"], data) # Путь до item
            
            show_sections(call.message.chat.id, USERS_INFO.get_user_info(call.from_user.id)["current_path"], call.message)




if __name__ == "__main__":
    # Запуск потока для периодического обновления
    # update_thread = threading.Thread(target=test_bot)
    # update_thread.daemon = True  # Поток будет остановлен при завершении основного потока
    # update_thread.start()


    # Загрузка списка пользователей
    ALLOWED_USERS = load_json("ALLOWED_USERS.json")


    bot.polling(none_stop=True)

