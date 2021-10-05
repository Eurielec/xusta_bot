"""
Handler functions for bot decorators
"""

# Import the bot interface
from bot import bot

# Import filters for permissions
from modules import filter

# Import for the camera
from modules import camera

# Import to log messages
from modules import logs

# Imports for cleaning functions
# from modules import batallon

# Imports for beeping the buzzer before recording camera
from modules import beep

# Imports for covid
from modules import covid

# Import for moving camera and capturing at the same time
import threading


class Handlers:

    def __init__(self):
        self.cam = camera.Camera()
        self.beeper = beep.Beeper()
        self.covid = covid.Covid()
        self.log = logs.Log()
        return

    def get_image_handler(self, message):
        if filter.check_auth(message) and filter.check_limits(message):
            self.log.log_message(message)
            self.beeper.get_image_advertise()
            self.cam.get_picture(message)
        return

    def get_video_handler(self, message):
        if filter.check_auth(message) and filter.check_limits(message):
            self.log.log_message(message)
            self.beeper.get_video_advertise()
            ff = self.cam.ffmpeg_video(5)
            t = threading.Thread(target=self.cam.get_video, args=(message, ff))
            t.start()
        return

    def get_salseo_handler(self, message):
        if filter.check_auth(message) and filter.check_limits(message):
            self.log.log_message(message)
            self.beeper.get_salseo_advertise()
            ff = self.cam.ffmpeg_video(15)
            t = threading.Thread(
                target=self.cam.get_salseo, args=(message, ff))
            t.start()
        return

    def get_nevera_handler(self, message):
        if filter.check_auth(message) and filter.check_limits(message):
            self.log.log_message(message)
            self.beeper.get_nevera_advertise()
            ff = self.cam.ffmpeg_video(15)
            t = threading.Thread(
                target=self.cam.get_nevera, args=(message, ff))
            t.start()
        return

    def reset_camera_handler(self, message):
        if filter.check_auth(message):
            self.cam.reset(message)
        return

    def test_handler(self, message):
        self.log.log_message(message)
        bot.send_message(message.chat.id, "Hi!")
        return

    def get_id_handler(self, message):
        self.log.log_message(message)
        bot.send_message(message.chat.id, str(message.chat.id))
        return

    def cast_handler(self, message):
        if filter.god_check_auth(message):
            self.log.log_message(message)
            bot.send_message(filter.groups[1], message.text[6:])
        return

    def get_current_people_handler(self, message):
        if filter.check_auth(message):
            self.log.log_message(message)
            current = self.covid.get_current_people()
            bot.send_message(message.chat.id, current)
        return

    """
    def get_turn_handler(self, message):
        if filter.check_auth(message) or filter.god_check_auth(message):
            self.log.log_message(message)
            result = batallon.find_turn()
            bot.send_message(message.chat.id, result)
        return

    def turn_done_handler(self, message):
        if filter.god_check_auth(message):
            self.log.log_message(message)
            bot.send_message(message.chat.id, "Let's see...")
            self.cam.get_basura(message)
            batallon.turn_status(True)
            bot.send_message(
                message.chat.id,
                "Marcado como 'done', /turnundo para desmarcar!")
        return

    def turn_undo_handler(self, message):
        if filter.god_check_auth(message):
            self.log.log_message(message)
            batallon.turn_status(False)
            bot.send_message(message.chat.id,
                                 "Marcado como no realizado")
        return
    """
