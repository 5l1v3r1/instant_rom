#!/usr/bin/python3

import re

import requests
from bs4 import BeautifulSoup


class InstantRom:
    def __init__(self, proxy=None):
        self._proxy = self.setup_proxy(proxy)
        self._headers = {'User-Agent': None}
        self._session = requests.Session()
        self._session.headers.update(self._headers)

    def setup_proxy(self, proxy):
        if proxy is None:
            return None
        return {'http': 'http://' + proxy, 'https': 'https://' + proxy}


    def search(self, query=input('Enter your query\n> ')):
        url = 'http://www.emuparadise.me/roms/search.php?query={}&section=roms'.format(query)
        r = self._session.get(url)
        roms = BeautifulSoup(r.content, 'html.parser').findAll(class_='roms')
        for i, rom in enumerate(roms):
            print('[{}] {}'.format(i, rom.get_text()))  #  TODO: make this prettier
            if i % 10 == 0 and i != 0:
                prompt = input('> ')
                if prompt.isnumeric():
                    return 'http://www.emuparadise.me' + roms[int(prompt)].find('a')['href']


if __name__ == '__main__':
    bot = InstantRom()
    x = bot.search()
    print(x)
