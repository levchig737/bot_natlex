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

<<<<<<< HEAD
=======
TEST=113
>>>>>>> 5b193fccd211bd937dd8618c8198ed3fc03211af

# Получение текущего пути к файлу бота
bot_directory = os.path.dirname(os.path.abspath(__file__))

PATH_TO_DOCS = "docs"

# Путь к папке с разделами и подразделами
BASE_DIR = os.path.join(bot_directory, PATH_TO_DOCS)


ALLOWED_USERS = []
ALLOWED_ADMINS = []
# USERS_INFO = {}



class UsersInfo:
    def __init__(self):
        self.__users_info = {}

    @property
    def users_info(self):
        return self.__users_info

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

    def load_admin_info(self, user_id, username):
        found_user = get_user_from_allowed_admins(username) 
        found_user["current_path"] = BASE_DIR

        self.add_user_info(int(user_id), found_user)

    """
    Проверка есть ли пользователь 
    """
    def check_user(self, user_id):
        if user_id in self.__users_info:
            return True
        else:
            return False


# Создаем объект класса UsersInfo
USERS_INFO = UsersInfo()

# Админы
ADMIN_INFO = UsersInfo()



"""
Класс опросов.
Создание опроса, сохранение, загрузка в json.
Отправка пользователю.
"""
class Survey:
    def __init__(self):
        self.__survey = {}
        self.date = ""
        self.__name_survey = ""
        self.__name_result = ""
        self.users = []
        self.path = os.path.join(BASE_DIR, "surveys")

    @property
    def survey(self):
        return self.__survey

    @survey.setter
    def survey(self, dict):
        self.__survey = dict.copy()

    @property
    def name_survey(self):
        return self.__name_survey
    
    @name_survey.setter
    def name_survey(self, name):
        if name.endswith('.json'):
            self.__name_survey = name
        else:
            self.__name_survey = name + ".json"
    
    def get_question(self):
        try:
            return self.survey["question"]
        except:
            print("Ошибка, нет вопроса в опросе")
            # return "Вопрос"
    
    def get_options(self):
        try:
            return self.survey["options"]
        except:
            print("Ошибка, нет ответов в опросе")
            # return ['1 ответ', '2 ответ', '3 ответ']
        
    def load_survey(self, name):
        try:
            self.name_survey = name
            with open(os.path.join(self.path, self.name_survey), "r", encoding="utf-8") as file:
                self.survey = json.load(file)
                return True
        except Exception as e:
            print("Ошибка при чтении данных из файла:", e)
            return False

    def save_survey(self):
        # Загружаем в json фалй
        try:
            with open(os.path.join(self.path, self.name_survey), "w", encoding="utf-8") as file:
                json.dump(self.survey, file, ensure_ascii=False, indent=4)
            print("Данные успешно записаны в файл:", self.path)
        except Exception as e:
            print("Ошибка при записи данных в файл:", e)

    def get_results(self):
       None

    def send_survey(self, chat_id):
        bot.send_poll(chat_id, question=self.get_question(), options=self.get_options())







survey = Survey()
# survey.survey = {
#     "question": "Какой ваш любимый цвет?",
#     "options": ["Красный", "Синий", "Зеленый"],
# }
# survey.name_survey = "testnауыа"


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
    user1_lower = username.lower()
    for user in ALLOWED_USERS:
        user2_lower = user["username"].lower()
        if user2_lower == user1_lower:
            found_user = user.copy()
            break

    return found_user


def get_user_from_allowed_admins(username):
    found_user = None
    user1_lower = username.lower()
    for user in ALLOWED_ADMINS:
        user2_lower = user["username"].lower()
        if user2_lower == user1_lower:
            found_user = user.copy()
            break

    return found_user
    



"""
Клавиатура пользователя
"""
def user_keyboard(id, text="Главное меню"):
    if text == None:
        text = "Главное меню"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Главное меню')

    markup.add(item1)
    bot.send_message(id, text, reply_markup=markup)




"""
Клавиатура админа
"""
def admin_keyboard(id, text="Главное меню"):
    if text == None:
        text = "Главное меню"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Режим пользователя')
    item2 = types.KeyboardButton('Отмена') 

    markup.add(item1, item2)
    bot.send_message(id, text, reply_markup=markup)




"""
Функция создания кнопок ползователя
"""
def create_user_keyboard(directory, path):
    keyboard = types.InlineKeyboardMarkup()
    for item in directory:
        button = types.InlineKeyboardButton(text=item, callback_data=item)
        keyboard.add(button)
    return keyboard


"""
Функция создания кнопок админа
"""
def create_admin_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    item1 = "Создать опрос"
    item2 = "Отправить опрос"
    button1 = types.InlineKeyboardButton(text=item1, callback_data=f"admin:{item1}")
    button2 = types.InlineKeyboardButton(text=item2, callback_data=f"admin:{item2}")
    
    keyboard.add(button1, button2)
    
    return keyboard




"""
Инициализируем пользователя
"""
def initilize_user(user_id, username, text=None):
    if USERS_INFO.check_user(user_id):
        return

    print(user_id)
    
    # Добавления пользователя в локальный словарь по user_id
    USERS_INFO.load_user_info(user_id, username)

    USERS_INFO.refresh_current_path(user_id)



"""
Инициализируем админа
"""
def initilize_admin(user_id, username, text=None):
    if ADMIN_INFO.check_user(user_id):
        return
    
    print(user_id)
    
    # Добавления пользователся в локальный словарь по user_id
    ADMIN_INFO.load_admin_info(user_id, username)

    ADMIN_INFO.refresh_current_path(user_id)




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
Фильтр пользователей доступа к боту
"""
def admin_allowed(func):
    def wrapper(message):
        user = get_user_from_allowed_admins(message.from_user.username)
        if user:
            func(message)
        else:
            bot.send_message(message.chat.id, "Вы не имеете доступа к боту")
    return wrapper



def create_survey(message):
    # Создаем опрос
    new_survey = Survey()
    
    # Запрашиваем у пользователя вопрос и варианты ответов
    bot.send_message(message.chat.id, "Введите вопрос для опроса:")
    bot.register_next_step_handler(message, lambda msg: admin(msg) if msg.text == "Отмена" else get_question(msg, new_survey))

def get_question(message, survey):
    # Сохраняем вопрос в опросе и запрашиваем варианты ответов
    survey.survey["question"] = message.text
    bot.send_message(message.chat.id, "Введите варианты ответов через запятую:")
    bot.register_next_step_handler(message, lambda msg: admin(msg) if msg.text == "Отмена" else get_options(msg, survey))

def get_options(message, survey):
    # Сохраняем варианты ответов в опросе и сохраняем опрос в файл
    options = [option.strip() for option in message.text.split(',')]
    survey.survey["options"] = options
    bot.send_message(message.chat.id, "Введите название опроса:")
    bot.register_next_step_handler(message, lambda msg: admin(msg) if msg.text == "Отмена" else save_survey_name(msg, survey))

def save_survey_name(message, survey):
    # Сохраняем название опроса и сохраняем опрос в файл
    survey.name_survey = message.text
    survey.save_survey()
    bot.send_message(message.chat.id, "Опрос успешно создан и сохранен.")

def send_survey_for_users(message):
    try:
        survey = Survey()
        bot.send_message(message.chat.id, "Введите название опроса:")
        bot.register_next_step_handler(message, lambda msg: admin(msg) if msg.text == "Отмена" else load_survey(message, msg.text, survey))

    except:
        print("Ошибка отправки опроса")
        bot.send_message(message.chat.id, "Ошибка отправки опроса")

def load_survey(message, name, survey):
    try:
        survey.name_survey = name
        survey.load_survey(name)
        for user in USERS_INFO.users_info:
            survey.send_survey(user)
    except:
        print("Ошибка загрузки опроса, проверьте его наличие")
        bot.send_message(message.chat.id, "Ошибка загрузки опроса, проверьте его наличие")



"""
Функция для обработки создания опроса
"""
@bot.message_handler(commands=['admin'])
@admin_allowed
def admin(message):
    initilize_user(message.from_user.id, message.from_user.username)
    initilize_admin(message.from_user.id, message.from_user.username)

    admin_keyboard(message.from_user.id)
    
    keyboard = create_admin_keyboard()
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=keyboard)

    # send_survey_for_users(message)



"""
Функция для обработки команды /start
"""
@bot.message_handler(commands=['start'])
@user_allowed
def start(message):

    # Создаем стартовое меню и пишем приветсвенное сообщение
    hello_message = f"Привет, {message.from_user.first_name}!"        
    initilize_user(message.from_user.id, message.from_user.username, hello_message)
    user_keyboard(message.from_user.id, hello_message)
    
    show_sections(message.chat.id, BASE_DIR)

    # survey.save_survey()
    # survey.load_survey("testnауыа.json")
    # survey.send_survey(message)




"""
Перехватчик и метод получения текстовых сообщений
"""
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.type == 'private': # Если личное сообщение, а не канал какой-то
        initilize_user(message.from_user.id, message.from_user.username)

        if message.text == "Главное меню":
            USERS_INFO.refresh_current_path(message.from_user.id)
            
            show_sections(message.chat.id, BASE_DIR)

        elif message.text == "Режим пользователя":
            initilize_user(message.from_user.id, message.from_user.username)
            user_keyboard(message.from_user.id)





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
        return

    # Если список не пуст, т.е. есть файлы с текстом
    if files:
        for file in files:
            with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
                description = f.read()
            
            bot.edit_message_text(chat_id=chat_id, message_id=message.message_id, text=description)
            USERS_INFO.refresh_current_path(message.chat.id)
    else:
        keyboard = create_user_keyboard(dirs, path)
        if message == None:  
            bot.send_message(chat_id, "Выберите раздел:", reply_markup=keyboard)
        else:
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=message.message_id, reply_markup=keyboard)




"""
Функция для обработки коллбэков кнопок
"""
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call): 
    if call.message:
        data = call.data      
  
        if data:
            admin = data.split(":")
            if admin[0] == "admin":
                if admin[1] == "Создать опрос":
                    create_survey(call.message)
                elif admin[1] == "Отправить опрос":
                    send_survey_for_users(call.message)
                
            else: # Если пользователь
                new_path = os.path.join(USERS_INFO.get_user_info(call.from_user.id)["current_path"], data) # Путь до item
                USERS_INFO.update_user_path(call.from_user.id, new_path)
                
                show_sections(call.message.chat.id, USERS_INFO.get_user_info(call.from_user.id)["current_path"], call.message)





if __name__ == "__main__":
    # Запуск потока для периодического обновления
    # update_thread = threading.Thread(target=test_bot)
    # update_thread.daemon = True  # Поток будет остановлен при завершении основного потока
    # update_thread.start()


    # Загрузка списка пользователей
    ALLOWED_USERS = load_json("ALLOWED_USERS.json")
    ALLOWED_ADMINS = load_json("ALLOWED_ADMINS.json")

    
    while True:
        try:
            bot.polling(none_stop=True)
            # break
        except Exception as e:
            print(e)
