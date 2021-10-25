"""
Interface for the bot, webhook and decorators
"""
# Imports to get enviroment variables
import os

# Import the chosen library
import telebot

# Import handlers for decorators
from modules import handler

# Import for logging (debug or info)
import logging

# Imports for webhook
from aiohttp import web


# VARIABLES


# Telegram bot token (provided by @BotFather on Telegram)
API_TOKEN = os.environ.get("TOKEN", "")

# Address where we are setting the webhook
WEBHOOK_HOST = os.environ.get("HOST", "example.org")
WEBHOOK_PORT = os.environ.get("PORT", 80)
WEBHOOK_LISTEN = os.environ.get("LISTEN", "0.0.0.0")

# External url where we want the callbacks to go (nginx)
WEBHOOK_URL_BASE = "https://{}".format(WEBHOOK_HOST)
WEBHOOK_URL_PATH = "/{}/".format(API_TOKEN)


# INITIALIZE BOT


# Create the bot
bot = telebot.TeleBot(API_TOKEN)


# Initialize the info level in logging
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


# If executed directly
if __name__ == "__main__":

    # Create the aiohttp framework server
    app = web.Application()

    # Create Handler instance
    h = handler.Handler()

    # Function to handle webhook calls

    async def handle(request):
        if request.match_info.get('token') == bot.token:
            request_body_dict = await request.json()
            update = telebot.types.Update.de_json(request_body_dict)
            bot.process_new_updates([update])
            return web.Response()
        else:
            return web.Response(status=403)

    # HANDLERS

    @bot.message_handler(commands=['getImage', 'getimage'])
    def handle_image(message):
        h.get_image_handler(message)
        return

    @bot.message_handler(commands=['getVideo', 'getvideo'])
    def handle_video(message):
        h.get_video_handler(message)
        return

    @bot.message_handler(commands=['getSalseo', 'getsalseo'])
    def handle_salseo(message):
        h.get_salseo_handler(message)
        return

    @bot.message_handler(commands=['getNevera', 'getnevera'])
    def handle_nevera(message):
        h.get_nevera_handler(message)
        return

    @bot.message_handler(commands=['test'])
    def test(message):
        h.test_handler(message)
        return

    @bot.message_handler(commands=['getid', 'getId'])
    def get_chat_id(message):
        h.get_id_handler(message)
        return

    @bot.message_handler(commands=['cast'])
    def cast(message):
        h.cast_handler(message)
        return

    @bot.message_handler(commands=['getcurrentpeople', 'getCurrentPeople', 'g'])
    def get_current_people(message):
        h.get_current_people_number_handler(message)
        return

    """
    @bot.message_handler(commands=['getturn', 'getTurn'])
    def get_turn(message):
        h.get_turn_handler(message)
        return

    @bot.message_handler(commands=['turndone', 'turnDone'])
    def turn_done(message):
        h.turn_done_handler(message)
        return

    @bot.message_handler(commands=['turnundo', 'turnUndo'])
    def turn_undo(message):
        h.turn_undo_handler(message)
        return
    """

    @bot.message_handler(commands=['camerareset', 'cameraReset'])
    def reset_camera(message):
        h.reset_camera_handler(message)
        return

    # WEBHOOK

    # Set the route and function to handle them for http callbacks
    app.router.add_post('/{token}/', handle)

    # Tell Telegram to remove previous webhooks (maybe we left one open)
    bot.remove_webhook()

    # Set webhook
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

    # Start aiohttp server
    web.run_app(
        app,
        host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT)
