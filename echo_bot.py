import telebot

bot = telebot.TeleBot("7515441235:AAFfx9jTzo2CKy0gvhFfhV-0xLTLtBHi6nU")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет, как дела?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
