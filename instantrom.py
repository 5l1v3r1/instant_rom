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

#    def select_console(self):
#        main_menu = []
#        r = self._session.get('http://www.emuparadise.me/roms-isos-games.php')
#        soup = BeautifulSoup(r.content, 'html.parser')
#        main_menu.append(soup.find(id='console'))
#        main_menu.append(soup.find(id='arcade'))
#        main_menu.append(soup.find(id='handheld'))
#        main_menu.append(soup.find(id='computer'))
#        main_menu.append(soup.find(id='other'))
#        for i, codeblock in enumerate(main_menu):
#           print('{} {}'.format(i, codeblock.find('h2').get_text().strip()))
#        prompt = int(input('> '))
#        links = main_menu[prompt].findAll('a')
#        for i, link in enumerate(links):
#            print('[{}] {}'.format(i, link.get_text()))
#        prompt = int(input('> '))
#        url = 'http://www.emuparadise.me{}'.format(links[prompt]['href'])
#        print(url)
#        r = self._session.get(url)
#        sys_id = ''
#        try:
#            sys_id = re.search(r'[/][0-9]+', url).group().replace('/', '')
#        except Exception as e:
#            print(e)
#            sys_id = None
#        if sys_id is None:  # failsafe
#            string = BeautifulSoup(r.content, 'html.parser').findAll(align='center')[1].find('a')['href']
#            sys_id = re.search(r'[/][0-9]+', string).group().replace('/', '')
#        print(sys_id)
#        return sys_id


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
