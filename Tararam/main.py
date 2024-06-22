import telebot
from telebot import types
import pandas as pd
from config import token
from parser1 import pars_1
from parser2 import pars_2

bot = telebot.TeleBot(token)

data = pd.DataFrame(columns=['user_id', 'event_type'])
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет! Я помогу вам выбрать идеальное место, где тебе вы сможете отметить свой праздник 🥳 или хорошо провести время 😄  ")
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('День рождения', callback_data='option1')
    itembtn2 = types.InlineKeyboardButton('Свадьба', callback_data='option2')
    itembtn3 = types.InlineKeyboardButton('Мальчишник', callback_data='option4')
    itembtn4 = types.InlineKeyboardButton('Встреча c друзьями', callback_data='option3')
    markup.add(itembtn1, itembtn2, itembtn3,itembtn4)
    bot.send_message(message.chat.id, "Укажите причину обращения ко мне 🤔 ", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['option1', 'option2', 'option3', 'option4'])
def handle_event_type(call):
    if call.data == 'option1':
        data.loc[len(data.index)] = {'user_id': call.from_user.id, 'event_type': 'День рождения', 'link': None}
        bot.send_message(call.message.chat.id, "Вы выбрали День рождения 🎂")
    elif call.data == 'option2':
        data.loc[len(data.index)] = {'user_id': call.from_user.id, 'event_type': 'Свадьба', 'link': None}
        bot.send_message(call.message.chat.id, "Вы выбрали свадьбу 👰")
    elif call.data == 'option3':
        data.loc[len(data.index)] = {'user_id': call.from_user.id, 'event_type': 'Встреча с друзьями', 'link': None}
        bot.send_message(call.message.chat.id, "Вы выбрали встречу с друзьями 😎")
    elif call.data == 'option4':
        data.loc[len(data.index)] = {'user_id': call.from_user.id, 'event_type': 'мальчишник', 'link': None}
        bot.send_message(call.message.chat.id, "Вы выбрали мальчишник 🕺")
    show_place_options(call.message)

def show_place_options(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Боулинг', callback_data='bowling')
    itembtn2 = types.InlineKeyboardButton('Лофты', callback_data='loft')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Выберите тип площадки", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'bowling')
def handle_bowling(call):
    global current_club_index  # Добавьте эту строку, чтобы использовать переменную
    current_club_index = 0  # Инициализируйте переменную
    show_club_info(call)


def show_club_info(call):
    global current_club_index
    all_club_data = pars_1()
    if current_club_index < len(all_club_data):
        club = all_club_data[current_club_index]
        response = f"*{club['name']}*\n"
        response += f"Метро: {', '.join(club['metro'])}\n"
        response += f"Цены:\n"
        for price_item in club['price']:
            response += f"- {price_item}\n"
        response += f"\n\n\n{club['url']}"
        bot.send_message(call.message.chat.id, response)
        current_club_index += 1
        show_place_options2(call.message)
    else:
        bot.send_message(call.message.chat.id, "Больше информации нет")


def show_place_options2(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Да', callback_data='Yes')
    itembtn2 = types.InlineKeyboardButton('Нет', callback_data='No')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Хотите еще", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'Yes')
def handle_yes(call):
    show_club_info(call)


@bot.callback_query_handler(func=lambda call: call.data == 'No')
def handle_no(call):
    show_place_options(call.message) 



@bot.callback_query_handler(func=lambda call: call.data == 'loft')
def handle_loft(call):
    global current_loft_index  # Добавьте эту строку, чтобы использовать переменную
    current_loft_index = 0  # Инициализируйте переменную
    show_loft_info(call)


def show_loft_info(call):
    global current_loft_index
    all_loft_data = pars_2()
    if current_loft_index < len(all_loft_data):
        loft = all_loft_data[current_loft_index]
        response = f"*{loft['name']}*\n"
        response += f"Метро: {', '.join(loft['metro'])}\n"
        response += f"Цены:\n"
        for price_item in loft['price']:
            response += f"- {price_item}\n"
        response += f"\n\n\n{loft['url']}"
        bot.send_message(call.message.chat.id, response)
        current_loft_index += 1
        show_place_options3(call.message)
    else:
        bot.send_message(call.message.chat.id, "Больше информации нет")


def show_place_options3(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Да', callback_data='Yes2')
    itembtn2 = types.InlineKeyboardButton('Нет', callback_data='No2')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Хотите еще", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'Yes2')
def handle_yes(call):
    show_loft_info(call)


@bot.callback_query_handler(func=lambda call: call.data == 'No2')
def handle_no(call):
    show_place_options(call.message) 


    


bot.infinity_polling()
data.to_csv('пользователи.csv')
df_from_csv = pd.read_csv('пользователи.csv')
df_from_csv
