# Import to get enviroment variables and check for files existence
import os

# Import to write to csv file
import csv


class Log:

    def __init__(self):
        """
        Create Log instance
        """
        # Logs file to write
        self.logs_file = os.environ.get("LOG_FILE", "logs/logs.csv")

    def check_csv(self):
        """
        Check the csv exists or create it
        """
        # Check if the log file exists
        if os.path.isfile(self.logs_file):
            return True
        # Create it if it doesn't exist
        else:
            open(self.logs_file, "w").close()
            self.write_csv_headers()
            return True

    def write_csv_headers(self):
        """
        Write headers to the csv
        """

        with open(self.logs_file, 'a', newline='') as f:
            writer = csv.writer(f)

            # Define the headers
            headers = ['ts', 'from_user_id', 'from_user_nick',
                       'from_user_name', 'from_user_surname', 'chat_id',
                       'message_id', 'type', 'text']

            # Write the headers
            writer.writerow(headers)
        return

    def write_csv_row(self, row):
        """
        Write a row to the csv
        """
        self.check_csv()
        with open(self.logs_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(row)
        return

    def log_message(self, message):
        """
        Write a message to logs
        """
        # Get the data
        ts = message.date
        from_user_id = message.from_user.id
        from_user_nick = message.from_user.username
        from_user_name = message.from_user.first_name
        from_user_surname = message.from_user.last_name
        chat_id = message.chat.id
        message_id = message.message_id
        type = message.chat.type
        text = message.text

        # Generate the row
        row = [ts, from_user_id, from_user_nick, from_user_name,
               from_user_surname, chat_id, message_id, type, text]

        # Write the row
        self.write_csv_row(row)
        return
