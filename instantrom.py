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
        url = 'http://www.doperoms.com/search.php?s={}&method=ROM+SEARCH'.format(query)
        r = self._session.get(url)
        roms = BeautifulSoup(r.content, 'html.parser').findAll(id='listing')
        for i, rom in enumerate(roms):
            if rom.get_text() == '':
                del(roms[i])
        for i, rom in enumerate(roms):
            print('[{}] {} | {}'.format(i, rom.get_text(), rom.find_next().find_next().get_text()))  # TODO: make this prettier
            if i % 10 == 0 and i != 0:
                prompt = input('> ')
                if 'q' in prompt:
                    print('quiting')
                    raise SystemExit
                if prompt.isnumeric():
                    return 'http://www.doperoms.com/' + roms[int(prompt)]['href']

    def download(self, url):
        r = self._session.get(url)


if __name__ == '__main__':
    bot = InstantRom()
    x = bot.search()
    print(x)
