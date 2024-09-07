import telebot
from datetime import datetime
import os

TOKEN = '7511399606:AAGJIue8oCS23J6rDtexqAXBc5fsPssNkdQ'
bot = telebot.TeleBot(TOKEN)

# Avtomatik javoblar
unavailable_message = "Hozirda Telegramda emasman, tez orada qaytaman."
available_message = "Hozir online man."

# Faylga xabarlarni yozish uchun
history_file = 'message_history.txt'

# Avtomatik javob rejimi (default: OFF)
auto_reply_enabled = False

# Faqat ma'lum vaqtda avtomatik javob berish (soat 18:00 - 09:00)
start_time = 18  # 18:00
end_time = 9    # 09:00

def save_message(message):
    with open(history_file, 'a') as file:
        file.write(f"{datetime.now()} - {message.from_user.first_name}: {message.text}\n")

def is_time_for_auto_reply():
    current_hour = datetime.now().hour
    return (current_hour >= start_time or current_hour < end_time)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Bu bot avtomatik javob beruvchi botdir.")

@bot.message_handler(commands=['enable_auto'])
def enable_auto_reply(message):
    global auto_reply_enabled
    auto_reply_enabled = True
    bot.send_message(message.chat.id, "Avtomatik javob yoqildi.")

@bot.message_handler(commands=['disable_auto'])
def disable_auto_reply(message):
    global auto_reply_enabled
    auto_reply_enabled = False
    bot.send_message(message.chat.id, "Avtomatik javob o'chirildi.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global auto_reply_enabled
    save_message(message)  # Xabar tarixini saqlash

    if auto_reply_enabled and is_time_for_auto_reply():
        bot.send_message(message.chat.id, unavailable_message)
    else:
        bot.send_message(message.chat.id, available_message)

if __name__ == '__main__':
    # Xabar tarixini faylda saqlashni boshlash
    if not os.path.exists(history_file):
        with open(history_file, 'w') as file:
            file.write("Xabarlar tarixi:\n")
    
    bot.polling(none_stop=True)
