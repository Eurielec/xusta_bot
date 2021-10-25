import os
import requests


class Covid:

    def __init__(self):
        """
        Create an instance of Covid (lol)
        """
        self.covid_endpoint = os.environ.get(
            'COVID_BACKEND_ENDPOINT', 'decovid.eurielec.etsit.upm.es')

    def get_current_people_number(self, club: str = "eurielec"):
        """
        Returns the number of people currently at the local.

        Parameters:
            * club (str): association.
        """
        try:
            r = requests.get('https://%s/current/number/%s' %
                             (self.covid_endpoint, club))
            if r.status_code == 200:
                return r.text
            else:
                return None
        except Exception:
            return None

    def get_current_people_email(self, club: str = "eurielec"):
        """
        Returns the emails of people currently at the local.
        Parameters:
            * club (str): association.
        """
        try:
            r = requests.get('https://%s/current/email/%s' %
                             (self.covid_endpoint, club))
            if r.status_code == 200:
                return r.text
            else:
                return None
        except Exception:
            return None
