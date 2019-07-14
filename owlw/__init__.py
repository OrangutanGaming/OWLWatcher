"""
MIT License

Copyright (c) 2019 Nihaal Sangha (Orangutan)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from selenium import webdriver
from time import sleep
from .http import HTTPSession

__version__ = '0.1.0'

class OWLWatcher:
    def __init__(self, client_id, *, profile_path=None):
        self.http = HTTPSession(client_id)
        self._watching = False
        self.ffprofile = webdriver.FirefoxProfile(profile_path)

    def start(self):
        while True:
            data = self.http.get_stream('overwatchleague')
            if data['data'] and not self._watching:
                driver = webdriver.Firefox(firefox_profile=self.ffprofile)
                driver.get("https://twitch.tv/overwatchleague")
                self._watching = True
            elif not data['data'] and self._watching:
                driver.close()
                self._watching = False
            sleep(600)   
