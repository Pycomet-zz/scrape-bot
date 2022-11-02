# filters
from telebot import apihelper
import asyncio
from tgbot.filters.admin_filter import AdminFilter

# handlers
from tgbot.handlers.admin import admin_user
from tgbot.handlers.spam_command import anti_spam
from tgbot.handlers.user import any_user

# middlewares
from tgbot.middlewares.antiflood_middleware import antispam_func

# states
from tgbot.states.register_state import Register

# utils
from tgbot.utils.database import Database

from tgbot.config import DEBUG, SERVER_URL, TOKEN

# telebot
import telebot
from telebot import TeleBot

# flask
from flask import Flask, request

# config
from tgbot import config

db = Database()

app = Flask(__name__)


# remove this if you won't use middlewares:
apihelper.ENABLE_MIDDLEWARE = True


# I recommend increasing num_threads
bot = TeleBot(config.TOKEN, num_threads=5)


# Set Webhook
@app.route("/" + TOKEN, methods=["POST", "GET"])
def checkWebhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "Your bot application is still active!", 200


@app.route("/")
def webhook():
    print("Trial")
    bot.remove_webhook()
    bot.set_webhook(url=SERVER_URL + "/" + TOKEN)
    return "Application running!", 200


def register_handlers():
    bot.register_message_handler(
        admin_user, commands=["start"], admin=True, pass_bot=True
    )
    bot.register_message_handler(
        any_user, commands=["start"], admin=False, pass_bot=True
    )
    bot.register_message_handler(anti_spam, commands=["spam"], pass_bot=True)


register_handlers()

# Middlewares
bot.register_middleware_handler(antispam_func, update_types=["message"])


# custom filters
bot.add_custom_filter(AdminFilter())


def run():
    print("Running")
    bot.infinity_polling()


def run_web():
    print("Running through web hook")
    app.run(host="0.0.0.0", threaded=True, port="5443", debug=True)


if DEBUG == True:
    run()
else:
    run_web()
