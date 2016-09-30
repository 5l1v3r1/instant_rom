#!/usr/bin/python3

import os
import zipfile

import requests
from bs4 import BeautifulSoup


class InstantRom:
    def __init__(self, proxy=None):
        self._session = requests.Session()
        self._session.proxies = self.setup_proxy(proxy)
        self._session.headers.update({'User-Agent': None})  #TODO: Add valud UA

    def setup_proxy(self, proxy):
        '''
        :param proxy: - http/https proxy
        :returns: proxy
        '''
        if proxy is None:
            proxy = {
                'http' : os.environ.get('HTTP_PROXY'),
                'https': os.environ.get('HTTPS_PROXY'),
                'ftp': os.environ.get('FTP_PROXY')
            }
            return proxy
        return {'http': 'http://' + proxy, 'https': 'https://' + proxy}

    def search(self, query=input('Enter your query\n> ')):
        '''
        :param: query = search query to find roms
        :returns: list of selected roms (to be downloaded)
        '''
        results = []
        url = 'http://www.doperoms.com/search.php?s={}&method=ROM+SEARCH'.format(query)
        r = self._session.get(url)
        roms = BeautifulSoup(r.content, 'html.parser').findAll(id='listing')
        for i, rom in enumerate(roms):
            if rom.get_text() == '':
                del(roms[i])
        print('y - yes (done) | n - next | q - quit')
        for i, rom in enumerate(roms):
            rom_name = rom.get_text()
            system = rom.find_next().find_next().get_text()
            print('[{}] {} | {}'.format(i, system, rom_name))
            if i % 10 == 0 and i != 0:
                prompt = input('> ')
                if 'q' in prompt:
                    print('quiting')
                    raise SystemExit
                if 'y' in prompt:
                    break
                if prompt.isnumeric():
                    url = 'http://www.doperoms.com/' + roms[int(prompt)]['href']
                    r = self._session.get(url)
                    url = 'http://www.doperoms.com' + BeautifulSoup(r.content, 'html.parser').center.find('a')['href']
                    r = self._session.get(url)
                    url = BeautifulSoup(r.content, 'html.parser').find(style='padding:15px; width: 400px; border:1px dashed #000000;').findAll('a')[1]['href']
                    result_name = roms[int(prompt)].get_text()
                    results.append(('http://www.doperoms.com' + url, result_name))
        return results

    def download(self, url, filename):
        '''
        downloads :param url: and saves it to :param filename:
        '''
        r = self._session.get(url)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        self.unzip(filename)

    def unzip(self, filename, delete=True):
        if zipfile.is_zipfile(filename):
            with zipfile.ZipFile(filename) as zip:
                zip.extractall()
        if delete is True:
            os.remove(filename)

    def queue(self):
        '''
        homebrew manager/queue
        '''
        q = self.search()
        for i in q:
            self.download(i[0], i[1])

if __name__ == '__main__':
    InstantRom().queue()
