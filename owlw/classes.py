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

import datetime
from time import sleep
from typing import Optional

import requests
from selenium import webdriver


class Stream:
    def __init__(self, *, title: str, user_id: str, user_name: str, game_id: int, type: str, started_at: str):
        self.user_id = user_id
        self.user_name = user_name
        self.game_id = game_id
        self.type = type
        self.title = title
        self.started_at: datetime.datetime = datetime.datetime.strptime(started_at, "%Y-%m-%dT%H:%M:%SZ")

    @classmethod
    def from_response(cls, response: dict) -> Optional['Stream']:
        data = response['data']
        if not data:
            return

        data = data[0]

        return cls(
            title=data['title'],
            game_id=data['game_id'],
            type=data['type'],
            started_at=data['started_at'],
            user_id=data['user_id'],
            user_name=data['user_name'],
        )


class HTTPSession:
    base = 'https://api.twitch.tv/helix'

    def __init__(self, client_id: str):
        self.client_id = client_id

    def request(self, method, url, *, params) -> dict:
        headers = {'Client-ID': self.client_id}
        url = self.base + url
        r = requests.request(method, url, params=params, headers=headers)
        return r.json()

    def get_stream(self, channel_name: str) -> Optional[Stream]:
        params = [('user_login', channel_name)]
        return Stream.from_response(self.request('GET', '/streams', params=params))


class OWLWatcher:
    channel_name = 'overwatchleague'

    def __init__(self, client_id: str, *, profile_path: str = None):
        self.http = HTTPSession(client_id)
        self.ffprofile = webdriver.FirefoxProfile(profile_path)
        self._watching = False

    def _check_title(self, title: str) -> bool:
        """Checks if the title matches a current game or a replay."""
        title = title.lower()
        for i in ('rewatch',):
            if i in title:
                return False
        return True

    def start(self, sleep_seconds: int = 600, *, once: bool = False):
        driver = None
        while True:
            stream = self.http.get_stream(self.channel_name)
            if stream and not self._watching and self._check_title(stream.title):
                # Live and not watching
                if driver is None:
                    driver = webdriver.Firefox(firefox_profile=self.ffprofile)
                driver.get(f"https://twitch.tv/{self.channel_name}")
                self._watching = True

            elif not stream and self._watching:
                # Offline and watching
                driver.close()

                if once is True:
                    return

                driver = None
                self._watching = False
            sleep(sleep_seconds)
