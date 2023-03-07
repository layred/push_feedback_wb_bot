from apps.bot.bots import Bot
from django.conf import settings
from django.core.management import BaseCommand
from django.utils import autoreload

bot = Bot()


def restart_bot():
    bot.enable_save_next_step_handlers()
    bot.load_next_step_handlers()
    while True:
        try:
            print(f'Бот {bot.get_me().first_name}(@{bot.get_me().username}) запущен!')
            bot.polling(none_stop=True, timeout=360)
        except Exception as e:
            print(f'Бот {bot.get_me().first_name}(@{bot.get_me().username}) перезапущен из-за ошибки')
            bot.logger.error(e, exc_info=True)
            continue


class Command(BaseCommand):
    help = 'Run Telegram BOT'

    def handle(self, *args, **kwargs):
        if settings.DEBUG:
            autoreload.run_with_reloader(restart_bot)
        else:
            restart_bot()


@bot.my_chat_member_handler(func=lambda member: member.new_chat_member.status == 'kicked')
def bot_kicked(member):
    bot.kick_user(member.from_user.id)


@bot.message_handler(content_types=['contact'])
def recieve_contact(message):
    try:
        if message.contact.user_id == message.from_user.id:
            bot.register_new_user(message)
        else:
            bot.register_next_step_handler(bot.send(message.chat.id, '<b>К сожалению, это не похоже на контакт, попробуйте отправить еще раз🤷🏼‍♂️</b>', bot.markups.register()), recieve_contact)
    except Exception as err:
        bot.logger.error(err, exc_info=True)
        bot.delete(message.chat.id, message.id)
        bot.send_error_message(message.chat.id)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        if bot.is_new_user(message):
            bot.send_register_message(message)
        else:
            bot.send_welcome_message(message)
    except Exception as err:
        bot.logger.error(err, exc_info=True)
        bot.delete(message.chat.id, message.id)
        bot.send_error_message(message.chat.id)


@bot.message_handler(commands=['my'], func=lambda message: bot.is_new_user(message) is False)
def my(message):
    try:
        bot.send_my_personals(message)
    except Exception as err:
        bot.logger.error(err, exc_info=True)
        bot.delete(message.chat.id, message.id)
        bot.send_error_message(message.chat.id)


@bot.message_handler(commands=['articles'], func=lambda message: bot.is_new_user(message) is False)
def articles(message):
    try:
        bot.send_tracked_articles(message)
    except Exception as err:
        bot.logger.error(err, exc_info=True)
        bot.delete(message.chat.id, message.id)
        bot.send_error_message(message.chat.id)


@bot.message_handler(commands=['settings'], func=lambda message: bot.is_new_user(message) is False)
def change_stars(message):
    try:
        bot.settings(message)
    except Exception as err:
        bot.logger.error(err, exc_info=True)
        bot.delete(message.chat.id, message.id)
        bot.send_error_message(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    try:
        if 'wb' in call.data:
            bot.process_wb(call)
        elif 'tracked_articles' in call.data:
            bot.process_tracked_articles(call)
        elif 'settings' in call.data:
            bot.settings_process(call)
    except Exception as err:
        bot.logger.error(err, exc_info=True)
        bot.delete(call.message.chat.id, call.message.message_id)
        bot.send_error_message(call.message.chat.id)
