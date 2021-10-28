"""
Camera module

This module is designed to handle the camera as a resource
"""

# Imports to access os
import os

# Imports to make http requests
import requests

# Imports to handle time
import time

# Imports to handle transcoding and conversion
from ffmpy import FFmpeg

# Import datetime for timing
import datetime

# Imports to handle locks
import threading

# Import to get the output of a command (and running it on the console)
import subprocess

import logging

# Import to send messages
from bot import bot


"""
Via web we can set some fixed positions of the camera, and call them via API
Also, inspecting element we can see the command corresponding the position:
Position 1 is 31, position 2 is 33, position 3 is 35 and so.
"""


class Camera:

    def __init__(self):
        """
        Create Camera instance
        """
        # Make sure nobody can access the camera resource at the same time
        self.cam_lock = threading.RLock()
        self.move_lock = threading.RLock()

        # Set the camera settings
        self.cam_ip = os.environ.get('CAM_IP', '10.0.0.242')
        self.cam_port = os.environ.get('CAM_PORT', '8080')
        self.cam_url = 'http://%s:%s/' % (self.cam_ip, self.cam_port)

        # Set the camera user and password
        self.cam_user = os.environ.get('CAM_USER', '')
        self.cam_password = os.environ.get('CAM_PASSWORD', '')

    def get_picture(self, message):
        """
        Get a still image from the camera

        Arguments:
            - message: to interact with the message
        """
        # Set the resource as not available
        self.cam_lock.acquire()
        # Get the snapshot (WANSCAM API)
        try:
            image = requests.get(
                '%ssnapshot.cgi' % (self.cam_url),
                auth=(self.cam_user, self.cam_password)).content
            bot.send_photo(message.chat.id, image)
        # Tell users to check the camera if an error occurs
        except Exception:
            bot.send_message(message.chat.id, "Camera seems to be offline")
        # Release the resource
        self.cam_lock.release()
        return

    def set_alias(self, message, alias):
        """
        Set camera alias

        Arguments:
            - alias: name to appear on the top left of the camera
        """
        # Set the alias (WANSCAM API)
        try:
            result = requests.get(
                '%sset_alias.cgi?user=%s&pwd=%s' % (self.cam_url),
                auth=(self.cam_user, self.cam_password)).content
            if result.status_code == 200:
                bot.send_photo(message.chat.id, "Done")
            else:
                bot.send_photo(message.chat.id, "Failed")
        # Tell users to check the camera if an error occurs
        except Exception:
            bot.send_message(message.chat.id, "Camera seems to be offline")
        return

    def reset(self, message):
        """
        Reset the camera

        Arguments:
            - message: to interact with the message
        """
        try:
            url = "%sreboot.cgi?user=%s&pwd=%s" % (
                self.cam_url, self.cam_user, self.cam_password)
            requests.get(url)
            bot.send_message(message.chat.id, "Camera is being reseted")
            time.sleep(60)
        except Exception:
            bot.send_message(message.chat.id, "Camera seems to be offline")
        return

    def move_to(self, position: int):
        """
        Move camera from current possition to another

        Arguments:
            - message: to interact with the message
        """
        pos = str(position)
        self.move_lock.acquire()
        url = '%sdecoder_control.cgi?user=%s&pwd=%s&onestep=0&command=%s' % (
            self.cam_url, self.cam_user, self.cam_password, pos)
        logging.info("URL", url)
        r = requests.get(url)
        logging.info("REQUEST RESULT", r.status_code, r.content)
        # It will always take less than 7 seconds
        time.sleep(7)
        self.move_lock.release()
        return 200

    def pan(self, _from: int, to: int):
        """
        Pan from current possition to another and back

        Arguments:
            - _from: position to (end really)
            - to: position to go in the middle
        """
        self.move_to(to)
        self.move_to(_from)
        return

    def get_video(self, message, ffmpeg):
        """
        Get a video from the camera (still)

        Arguments:
            - message: to interact with the message
            - ffmpeg: object to transcode
        """
        self.cam_lock.acquire()
        try:
            ffmpeg.cmd
            video, stderr = ffmpeg.run(stdout=subprocess.PIPE)
            bot.send_video(message.chat.id, video)
        except Exception:
            bot.send_message(message.chat.id, "Camera seems to be offline")
        self.cam_lock.release()
        return

    def get_salseo(self, message, ffmpeg):
        """
        Get a video with panning movement (to the sofa and back to the door)

        Arguments:
            - message: to interact with the message
            - ffmpeg: object to transcode
        """
        self.cam_lock.acquire()
        try:
            dt_1 = datetime.datetime.now()
            ffmpeg.cmd
            t = threading.Thread(target=self.pan, args=(31, 33))
            t.start()
            video, stderr = ffmpeg.run(stdout=subprocess.PIPE)
            dt_2 = datetime.datetime.now()
            if (dt_2 - dt_1) > datetime.timedelta(seconds=22):
                bot.send_message(message.chat.id,
                                 "Camera working abnormally")
                self.reset(message)
            bot.send_video(message.chat.id, video)
        except Exception as e:
            logging.error(e)
            bot.send_message(message.chat.id, "Camera seems to be offline")
        self.cam_lock.release()
        return

    def get_nevera(self, message, ffmpeg):
        """
        Get a video with panning (to the fridge and back to the door)

        Arguments:
            - message: to interact with the message
            - ffmpeg: object to transcode
        """
        self.cam_lock.acquire()
        try:
            ffmpeg.cmd
            t = threading.Thread(target=self.pan, args=(31, 35))
            t.start()
            video, stderr = ffmpeg.run(stdout=subprocess.PIPE)
            bot.send_video(message.chat.id, video)
        except Exception:
            bot.send_message(message.chat.id, "Camera seems to be offline")
        self.cam_lock.release()
        return

    def get_basura(self, message):
        """
        Get a still image of the trash and frige

        Arguments:
            - message: to interact with the message
        """
        self.cam_lock.acquire()
        try:
            self.move_to(35)
            self.get_picture(message)
            self.move_to(31)
        except Exception:
            bot.send_message(message.chat.id, "Camera seems to be offline")
        self.cam_lock.release()
        return

    def ffmpeg_video(self, timeleft: int):
        """
        FFMPEG object to recording and piping the output

        Arguments:
            - timeleft: duration in seconds
        """
        return FFmpeg(
            inputs={
                '%svideostream.cgi?user=%s&pwd=%s&resolution=32&rate=1' % (
                    self.cam_url,
                    self.cam_user,
                    self.cam_password): """
                    -r 20 -t %s -hide_banner -loglevel panic""" % (timeleft)},
            outputs={
                'pipe:1': """
                -movflags frag_keyframe+empty_moov -c:v h264 -r 20 -f mp4"""})
