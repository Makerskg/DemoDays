# импортируем библиотеки для работы
from token_for_bot import TOKEN
import telebot
from telebot import types
import random

# устанавливаем связь с определенным ботом
token = TOKEN
bot = telebot.TeleBot(token)

# количество попыток для игры
attempts = 3

# создание клавиатуры
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
k1 = types.KeyboardButton('Играть')
k2 = types.KeyboardButton('Нет')
keyboard.add(k1, k2)

# функция, которая реагирует на первые команды для запуска бота,
# задает вопрос пользователю и выводит клавиатуру для ответа
@bot.message_handler(commands=['start', 'hello'])
def start_message(message):
    # сгенерировали случайное число
    random_int = random.choice(list(range(1,11)))
    print(random_int)
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'Привет {message.chat.first_name}, начнем игру?', reply_markup=keyboard)
    bot.register_next_step_handler(msg, get_start, random_int)

# функция, проверяющая ответ пользователя
def get_start(message, random_int):
    chat_id = message.chat.id
    if message.text == 'Играть':
        msg = bot.send_message(chat_id, f'Ок, тогда вот правила, правило только одно: \n нужно угадать число от 1 до 10 за три попытки /ok')
        bot.register_next_step_handler(message, game, attempts, random_int)
    else:
        bot.send_message(chat_id, f'До встречи в следующий раз {message.chat.first_name}!')

# функция вычитает одну попытку и принимает ответ от пользователя
def game(message, attempts, random_int):
    attempts = attempts - 1
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, f'Погнали, выбери число от 1 до 10 ...')
    bot.register_next_step_handler(msg, check_answer, attempts, random_int)

# функция проверяет ответ от пользователя, в зависимости от него выводит сообщение о победе, 
# либо запускает снова предыдущую функцию, и так до тех пор пока не закончатся попытки
def check_answer(message, attempts, random_int):
    chat_id = message.chat.id
    # проверили совпадает ли ответ с загаданным числом
    if message.text != str(random_int):
        msg = bot.send_message(chat_id, f'Все фигня, давай по-новой')
        # проверяем остались ли попытки
        if attempts == 0:
            msg = bot.send_message(chat_id, f'У вас закончились все попытки...\n'
                                            'Начать заново? /start')
            bot.register_next_step_handler(msg, start_message)
        else:
            game(msg, attempts, random_int)
    else:
        msg = bot.send_message(chat_id, f'Вы победили!!! Начать с начала /start\n'
                                        '/end для завершения')

# запускает бот и держит его в активном состоянии
bot.polling(none_stop=True, timeout=3600)