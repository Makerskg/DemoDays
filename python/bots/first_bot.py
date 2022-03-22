import telebot

token = ''

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'hi'])
def start_message(message):
    bot.send_message(message.chat.id, "Hello")

@bot.message_handler(content_types=['sticker'])
def send_sticker(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)

bot.polling()