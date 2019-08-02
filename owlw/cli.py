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

from typing import Optional

import click

from .classes import OWLWatcher


def _status(text: str, newline: bool = False):
    m = "\r" + text + "\033[K"
    click.echo(m, nl=newline)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--once', is_flag=True,
              help='If this option is given, it will only run until the end of the next stream.')
@click.option('--firefox-profile-path',
              help='The path to your Firefox Profile.')
@click.option('--sleep-time', default=600, type=int,
              help='The number of seconds to wait before checking the stream status again. Defaults to 600 seconds.')
@click.argument('client_id', required=True, type=str)
def run(once: bool, firefox_profile_path: Optional[str], sleep_time: int, client_id: str):
    OWLWatcher(client_id, profile_path=firefox_profile_path).start(sleep_time, once=once)
