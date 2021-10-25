import os
import requests


class Covid:

    def __init__(self):
        """
        Create an instance of Covid (lol)
        """
        self.covid_endpoint = os.environ.get(
            'COVID_BACKEND_ENDPOINT', 'decovid.eurielec.etsit.upm.es')

    def get_current_people(self, club: str = "eurielec"):
        """
        Returns the number of people currently at the local
        """
        try:
            r = requests.get('https://%s/current/%s' %
                             (self.covid_endpoint, club))
            if r.status_code == 200:
                return r.text
            else:
                return None
        except Exception:
            return None
