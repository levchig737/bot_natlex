import telebot
from telebot import types
import random

TOKEN = ''
ALLOWED_USERNAMES = []

bot = telebot.TeleBot(TOKEN)


"""
Основное меню    
"""
def main_menu(id, text):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Новости')
    item2 = types.KeyboardButton('Проекты')
    item3 = types.KeyboardButton('О компании')
    item4 = types.KeyboardButton('Другое')

    markup.add(item1, item2, item3, item4)
    bot.send_message(id, text, reply_markup=markup)




@bot.message_handler(func=lambda message: message.from_user.username not in ALLOWED_USERNAMES)
def some(message):
   bot.send_message(message.chat.id, "Прости, нет доступа")




"""
Перехватчик команды start, вывод меню
"""
@bot.message_handler(commands=['start'])
def start(message):
    # Создаем стартовое меню и пишем приветсвенное сообщение
    hello_message = f"Привет, {message.from_user.first_name}!"        
    main_menu(message.chat.id, hello_message)




"""
Перехватчик и метод получения текстовых сообщений
"""
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.chat.type == 'private': # Если личное сообщение, а не канал какой-то
        
        if message.text == "Новости":
            bot.send_message(message.chat.id, "Какие-то новости") #TODO парсинг из файла

        elif message.text == "Проекты":
            keyboard = types.InlineKeyboardMarkup()
            # По очереди готовим текст и обработчик для каждого знака зодиака
            key_android = types.InlineKeyboardButton(text='Мобильное приложение', callback_data='btn1')
            keyboard.add(key_android)

            key_income  = types.InlineKeyboardButton(text='Приложение учета доходов', callback_data='btn2')
            keyboard.add(key_income)
            
            key_new_buttons  = types.InlineKeyboardButton(text='Другие кнопочки', callback_data='new_buttons')
            keyboard.add(key_new_buttons)  

            # Показываем все кнопки сразу и пишем сообщение о выборе
            bot.send_message(message.from_user.id, text='Проекты', reply_markup=keyboard)

        elif message.text == "О компании":
            bot.send_message(message.chat.id, "О компании")
            bot.send_message(message.chat.id, """
    Компания «Натлекс» — аутсорс-компания, основанная в 2016 году. Нашим основным направлением является разработка веб и мобильных приложений.
    
    Развитие долгосрочных отношений с клиентами, создание качественного программного обеспечения — важнейшие принципы нашей работы. Мы выполняем все работы по основным этапам «жизненного цикла» программного обеспечения: анализ, планирование, проектирование и дизайн, разработка, тестирование, развертывание и поддержка. При работе используем Agile-методологии, что позволяет упростить прогнозирование затрат и показателей рентабельности проектов.
    
    Мы постоянно учимся новому, заботимся о работниках. В нашей интернациональной команде более 50 человек.
    
    Компания имеет аккредитацию в соответствии с постановлением Правительства РФ от 30.09.2022 № 1729.
    (Код ОКВЭД: 62.01)
""")

        elif message.text == "Другое":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Рандомное число')
            item2 = types.KeyboardButton('Бросить кубик🎲')
            item3 = types.KeyboardButton('Мой никнейм')
            back = types.KeyboardButton('Назад')

            markup.add(item1, item2, item3, back)

            bot.send_message(message.chat.id, "Проекты", reply_markup=markup)
        
        elif message.text == "Рандомное число":
            bot.send_message(message.chat.id, random.randint(0,10000))

        elif message.text == "Бросить кубик🎲":
            bot.send_dice(message.chat.id, "🎲")

        elif message.text == "Мой никнейм":
            bot.send_message(message.chat.id, message.from_user.username)

        elif message.text == "Назад":
            main_menu(message.chat.id, "Назад")  


""" 
Обработчик нажатий на кнопки Проекты
"""
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == "btn1":
            msg = "Инфа про мобильное приложений..."
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg)

        elif call.data == "btn2":
            msg = "Инфа про приложений учета доходов..."
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=msg)

        
        elif call.data == "new_buttons":
            keyboard = types.InlineKeyboardMarkup()
            key1 = types.InlineKeyboardButton(text='Кнопка 1', callback_data='btn11')
            keyboard.add(key1)
            key2 = types.InlineKeyboardButton(text='Кнопка 2', callback_data='btn11')
            keyboard.add(key2)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Другие кнопочки', reply_markup=keyboard)

        elif call.data == "btn11":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Кнопки удалены')



# Цикл проверки сообщений
bot.polling(none_stop=True, interval=0)