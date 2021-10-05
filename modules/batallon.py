# Imports for Google Drive Sheet
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Import to handle dates
import datetime

# Formatting mask for dates in Turnos de Basura Google's Sheet
datemask = "%d/%m/%Y"

# Spreadsheet linking
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


# Authenticate onto spreadsheet for a particular sheet
def auth_spreadsheet():
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            'secreto.json', scope)
        client = gspread.authorize(credentials)
        sheet = client.open("Turnos basura").sheet1
        return sheet
    except Exception:
        return


# Turns for taking the trash out
def find_turn():

    # Authenticate
    sheet = auth_spreadsheet()

    # Get current date
    today = datetime.datetime.today()
    try:

        # Go backwards trying to find the date in the spreadsheet
        for i in range(10):
            try:

                days_back = datetime.timedelta(i)
                find = sheet.find((today-days_back).strftime(datemask))
                row = find.row
                name = sheet.cell(row, 1).value
                surname = sheet.cell(row, 2).value
                full_name = "%s %s" % (name, surname)

                # Check if the turn is done
                if sheet.cell(row, 5).value == "done":
                    return "Le toca a %s, pero ya lo hizo" % full_name
                return "Le toca a %s" % full_name
            # Do nothing if we don't find the date, try next date
            except Exception:
                pass
    # Maybe not able to find a turn at all
    except Exception:
        return "I couldn't find a turn! Check the spreadsheet's date format"


# Check trash turn as done
def turn_status(boolean):

    # Authenticate
    sheet = auth_spreadsheet()

    # Get current date
    today = datetime.datetime.today()
    try:
        # Iterate dates backwards
        for i in range(10):
            try:
                days_back = datetime.timedelta(i)
                find = sheet.find((today-days_back).strftime(datemask))
                row = find.row
                value = 'done' if boolean is True else ''
                # Mask turn as done
                sheet.update_cell(row, 5, value)
                return "Ya ves"
            # Keep looking if date not found
            except Exception:
                pass
    # Date wasn't found at all
    except Exception:
        return "I couldn't mark it as done :("
