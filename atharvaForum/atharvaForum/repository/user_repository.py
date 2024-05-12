import os

import requests
import json
from atharvaForum.constants import AUTH_URL, HEADERS, getCredentials

class UserRepository:

    def __init__(self):
        pass

    @classmethod
    def getToken(self):
        res = requests.post(AUTH_URL, headers = HEADERS, data = json.dumps(getCredentials()),timeout=30)
        return res.json()['id_token']

