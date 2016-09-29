#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup


class InstantRom:
    def __init__(self, proxy=None):
        self._proxy = self.setup_proxy(proxy)
        self._headers = {}
        self._session = requests.Session()

    def setup_proxy(self, proxy):
        if proxy is None:
            return None
        return {'http': 'http://' + proxy, 'https': 'https://' + proxy}


    def search(self, query):


