#!/usr/bin/env python3

import pdb
import datetime

from urllib.parse import urlsplit

from .. import PluginBase


class Hastebin(PluginBase):

    site = 'hastebin'

    def __init__(self, url):
        super().__init__()
        self.original_url = url
        base_url = "http://hastebin.com/raw/{0}"

        split = urlsplit(url)

        paste_id = split.path.split('.')[0].split('/')[-1]

        self.id_list = [paste_id]
        self.content_urls = [base_url.format(paste_id)]

    def _post_get_content(self, responses):
        if not all(x.ok for x in responses):
            self._empty_handler()
            return

        self.items = 1
        self.titles = [None]
        self.ext_list = [None]
        self.timestamps = [datetime.datetime.fromtimestamp(0)]
        self.content_title = [None]
        self.content_filenames = self.id_list
