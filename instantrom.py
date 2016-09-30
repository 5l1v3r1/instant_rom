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
            rom_name = rom.get_text()
            system = rom.find_next().find_next().get_text()
            print('[{}] {} | {}'.format(i, system, rom_name))
            if i % 10 == 0 and i != 0:
                prompt = input('> ')
                if 'q' in prompt:
                    print('quiting')
                    raise SystemExit
                if prompt.isnumeric():
                    url = 'http://www.doperoms.com/' + roms[int(prompt)]['href']
                    print(url)
                    r = self._session.get(url)
                    url = 'http://www.doperoms.com' + BeautifulSoup(r.content, 'html.parser').center.find('a')['href']
                    print(url)
                    r = requests.get(url)
                    url = BeautifulSoup(r.content, 'html.parser').find(style='padding:15px; width: 400px; border:1px dashed #000000;').findAll('a')[1]['href']
                    return 'http://www.doperoms.com' + url

    def download(self, url):
        r = self._session.get(url)


if __name__ == '__main__':
    bot = InstantRom()
    x = bot.search()
    print(x)
