import telebot
import random

# Токен вашего Telegram-бота
TOKEN = "7105462304:AAH75YV6fmKmXyZHBQ-Xd26sPnws4G-UtKs"
bot = telebot.TeleBot(TOKEN)

# Максимальное количество участников
MAX_PARTICIPANTS = 10

# Список участников
participants = []

# ID пользователей, которые могут использовать команду /random
ALLOWED_USERS = [1328197458, 156420710]

# Команда /start для запуска бота
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Нажмите /join, чтобы добавить себя в список участников. Максимум 10 человек.\n"
                          "Чтобы рандомно выбрать участников, используйте /random (доступно только для админов).")

# Команда /join для добавления в список участников
@bot.message_handler(commands=['join'])
def join_queue(message):
    user = message.from_user

    if len(participants) < MAX_PARTICIPANTS:
        if user.full_name not in participants:
            participants.append(user.full_name)
            bot.reply_to(message, f"{user.full_name}, ты добавлен(а) в список!")
        else:
            bot.reply_to(message, "Ты уже в списке!")
    else:
        bot.reply_to(message, "Список уже полон (максимум 10 человек).")

# Команда /random для случайного выбора участников (доступна только админам)
@bot.message_handler(commands=['random'])
def random_participants(message):
    user_id = message.from_user.id

    if user_id not in ALLOWED_USERS:
        bot.reply_to(message, "У вас нет прав для использования этой команды.")
        return

    if len(participants) == 0:
        bot.reply_to(message, "В списке пока нет участников.")
        return

    selected = random.sample(participants, len(participants))
    response = "Вот случайный порядок выхода к доске:\n"
    for i, name in enumerate(selected, 1):
        response += f"{i}. {name}\n"

    bot.send_message(message.chat.id, response)

# Команда /list для отображения текущих участников
@bot.message_handler(commands=['list'])
def list_participants(message):
    if len(participants) == 0:
        bot.reply_to(message, "Список пуст.")
        return

    response = "Текущий список участников:\n"
    for i, name in enumerate(participants, 1):
        response += f"{i}. {name}\n"

    bot.send_message(message.chat.id, response)

# Команда /clear для очистки списка участников
@bot.message_handler(commands=['clear'])
def clear_participants(message):
    participants.clear()
    bot.reply_to(message, "Список участников был очищен.")

# Запуск бота
bot.polling(none_stop=True)
