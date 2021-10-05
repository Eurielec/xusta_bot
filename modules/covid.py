import os
import requests


class Covid:

    def __init__(self):
        """
        Create an instance of Covid (lol)
        """
        self.covid_endpoint = os.environ.get(
            'COVID_BACKEND_ENDPOINT', 'decovid.eurielec.etsit.upm.es')

    def get_current_people(self):
        """
        Returns the number of people currently at the local
        """
        r = requests.get('https://%s/current' % self.covid_endpoint)
        return r.text
