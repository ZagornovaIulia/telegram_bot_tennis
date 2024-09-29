from datetime import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand
import telebot
from telegram_users.models import TelegramUser
from schedules.models import Schedule

bot = telebot.TeleBot("7515441235:AAFfx9jTzo2CKy0gvhFfhV-0xLTLtBHi6nU")


def parse_datetime(args):
    date_string = args[0]
    time_string = args[1]
    datetime_string = f"{date_string} {time_string}"
    return datetime.strptime(datetime_string,  "%d:%m:%Y %H")


def get_or_create_user(message):
    user, created = TelegramUser.objects.get_or_create(
        id=message.from_user.id,
        defaults={
            'username': message.from_user.username,
            'last_name': message.from_user.last_name,
            'first_name': message.from_user.first_name
        }
    )
    return user


@bot.message_handler(commands=['book'])
def book(message):
    args = message.text.split()[1:]
    if len(args) < 2:
        bot.reply_to(message, "Пожалуйста, укажите дату и время.")

    try:
        date = parse_datetime(args)
    except ValueError:
        bot.reply_to(
            message, "Неверный формат даты или времени. Пожалуйста, укажите дату и время в формате: ДД:ММ:ГГГГ ЧЧ")
        return

    user = get_or_create_user(message)
    date_str = date.strftime("%Y-%m-%d %H:%M")

    if not Schedule.objects.filter(date=date).exists():
        schedule = Schedule.objects.create(date=date)
        schedule.users.add(user)

        bot.reply_to(message, f"Добавлено расписание на {date_str}")
    else:
        bot.reply_to(message, f"Расписание на дату {date_str} уже есть")


@bot.message_handler(commands=['unbook'])
def unbook(message):
    args = message.text.split()[1:]

    if len(args) < 2:
        bot.reply_to(
            message, "Неверный формат даты или времени. Пожалуйста, укажите дату и время в формате: ДД:ММ:ГГГГ ЧЧ")
        return

    try:
        date = parse_datetime(args)
    except ValueError:
        bot.reply_to(
            message, "Неверный формат даты или времени. Пожалуйста, укажите дату и время в формате: ДД:ММ:ГГГГ ЧЧ")
        return

    user = get_or_create_user(message)
    date_str = date.strftime("%Y-%m-%d %H:%M")

    if not user.schedules.filter(date=date).exists():
        bot.reply_to(message, f"Запись на дату {date_str} не найдена.")
        return
    else:
        user.schedules.filter(date=date).delete()
        bot.reply_to(message, f"Вы успешно удалили запись на {date_str}.")


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def handle(self, *args, **options):
        print('run bot')
        bot.infinity_polling()
