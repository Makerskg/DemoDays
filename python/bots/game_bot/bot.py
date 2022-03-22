import telebot
from telebot import types
import random

token = ''
bot = telebot.TeleBot(token)

attempts = 3

#start keyboard
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
k1 = types.KeyboardButton('Играть')
k2 = types.KeyboardButton('Нет')
keyboard.add(k1, k2)

@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    random_int = random.choice(range(1,11))
    print(random_int)
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'Привет {message.chat.first_name}, начнем игру?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, get_start, random_int)

def get_start(message, random_int):
    chat_id = message.chat.id
    if message.text == 'Играть':
        msg = bot.send_message(chat_id, f'Ок, тогда вот правила, правило только одно: \n нужно угадать число от 1 до 10 за три попытки')
        game(message, attempts, random_int)
    else:
        bot.send_message(chat_id, f'До встречи в следующий раз {message.chat.first_name}!')

def game(message, attempts, random_int):
    attempts = attempts - 1
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'Погнали, выбери число от 1 до 10 ...')
    bot.register_next_step_handler(msg, check_answer, attempts, random_int)

def check_answer(message, attempts, random_int):
    chat_id = message.chat.id
    if message.text != str(random_int):
        msg = bot.send_message(chat_id, f'Все фигня, давай по-новой')
        if attempts == 0:
            msg = bot.send_message(chat_id, f'У вас закончились все попытки...\nНачать заново? /start')
            bot.register_next_step_handler(msg, start_message)
        else:
            game(msg, attempts, random_int)
    else:
        msg = bot.send_message(chat_id, f'Вы победили!!! Начать с начала /start\n/end для завершения')

bot.polling(none_stop=True, timeout=3600)
