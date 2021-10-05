"""
This module is intended for filtering requests, with whitelists, blacklists,
groups, and so on. This way we can limit the access to resources.
"""

# Import to get environ variables
import os

# Import to send messages
from bot import bot

# Import to handle time limits and others
import datetime


class Filter:

    def __init__(self):
        """
        Create an instance of Filter
        """
        # Get the ids string
        self.groups_string = os.environ.get("GROUPS", "")
        self.godmode_string = os.environ.get("GODMODE", "")

        # Convert the string to lists
        self.groups = [int(v) for v in self.groups_string.split(",")]
        self.godmode = [int(v) for v in self.godmode_string.split(",")]

        # Get camera access limits
        self.times_a_day = int(os.environ.get("TIMES_A_DAY", 3))
        self.get_interval = int(os.environ.get("GET_INTERVAL", 15))
        self.last_camera_access = {"dt": datetime.datetime.fromtimestamp(0)}

        # Dictionary holding the last 3 requests' timestamps of every user (if requested >= 3)
        self.requests = {}

        # Define a 24h delta (for 3 requests per day limit)
        self.delta = datetime.timedelta(days=1)

        # Define a X minutes interval delta for density filter (do not access camera too often)
        self.density_delta = datetime.timedelta(minutes=self.get_interval)

    def check_auth(self, message):
        """
        Check the auth of a chat.id (forbid a user from accessing the camera via private chat)
        """
        # Check if chat.id in gods or allowed groups
        chat_id = message.chat.id
        user_id = message.from_user.id
        if (chat_id in self.groups) or (chat_id in self.godmode) or (user_id in self.godmode):
            return True
        # Send permissions notification always
        bot.send_message(chat_id, "You do not have enough permissions")
        return False

    def god_check_auth(self, message, flush_chat=True):
        """
        Check the auth for gods, special permissions everywhere, (private chat and groups)
        """
        # Check if user in gods
        chat_id = message.chat.id
        user_id = message.from_user.id
        if (user_id in self.godmode):
            return True
        # Send permission notification only if needed
        if flush_chat:
            bot.send_message(chat_id, "You do not have enough permissions")
        return False

    def check_last_access(self, message):
        """
        Check the last access to the camera (density filter)
        """
        # Get current time
        now = datetime.datetime.now()
        # Get last access
        last_access = self.last_camera_access.get("dt")
        # True if the access was longer than X minutes ago
        if last_access < (now - self.density_delta):
            self.last_camera_access["dt"] = now
            return True
        # Deny camera access otherwise
        else:
            bot.send_message(message.chat.id,
                             "Check the last camera update above or wait")
            return False

    # Check user limits

    def check_limits(self, message):
        # Always allow if the user is a god
        if self.god_check_auth(message, flush_chat=False):
            return True
        # Do not allow if the camera was accessed less than X minutes ago
        if self.check_last_access(message) is False:
            return False
        # Get the user id
        id = str(message.from_user.id)
        # Get current time
        now = datetime.datetime.now()

        # If the user has past requests, check the last request
        if id in self.requests.keys():
            timestamps = self.requests.get(id)
            # Check if the user has more than times_a_day requests
            if len(timestamps) >= self.times_a_day:
                oldest = timestamps[0]
                # If the oldest request was more than a day ago (and more than 3 past requests)
                if oldest < (now - self.delta):
                    # Update last 3 requests with the last one
                    timestamps.pop(0)
                    timestamps.append(now)
                    self.requests[id] = timestamps
                    return True
                # If the request is within 24h of the others, do not allow access
                else:
                    bot.send_message(message.chat.id,
                                     "You have exceeded daily access")
                    return False
            # If the user is new, create it on the dictionary
            else:
                timestamps.append(now)
                self.requests[id] = timestamps
                return True
        else:
            self.requests[id] = [now]
            return True
