# Import to run console command
import subprocess

# Import to wait
import time


class Beeper:

    def __init__(self):
        return

    @staticmethod
    def get_salseo_advertise():
        """
        Notify by beeping about getsalseo
        """
        # Beep 3 times, 250ms beeps, spaced by 200ms
        subprocess.call(["beep", "-f", "2100", "-l",
                        "250",  "-d",  "200", "-r", "3"])
        time.sleep(2)
        return

    @staticmethod
    def get_nevera_advertise():
        """
        Notify by beeping about getnevera
        """
        # Beep 3 times, 250ms beeps, spaced by 200ms
        subprocess.call(["beep", "-f", "2100", "-l",
                        "250",  "-d",  "200", "-r", "3"])
        time.sleep(2)
        return

    @staticmethod
    def get_image_advertise():
        """
        Notify by beeping about getimage
        """
        # Beep 3 times, 250ms beeps, spaced by 200ms
        subprocess.call(["beep", "-f", "2100", "-l",  "750"])
        time.sleep(2)
        return

    @staticmethod
    def get_video_advertise():
        """
        Notify by beeping about getimage
        """
        # Beep 3 times, 250ms beeps, spaced by 200ms
        subprocess.call(["beep", "-f", "2100", "-l",  "750"])
        time.sleep(2)
        return
