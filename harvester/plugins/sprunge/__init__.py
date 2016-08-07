#!/usr/bin/env python3

import pdb
import requests
import datetime

from urllib.parse import urlsplit

from .. import PluginBase

class Sprunge(PluginBase):

    site = 'sprunge'
    errormsg_template = "{id} not found."

    def __init__(self, url):
        super().__init__()
        self.original_url = url

        split = urlsplit(url)

        paste_id = split.path[1:]

        self.ext_list = [None]
        self.id_list = [paste_id]
        self.content_filenames = self.id_list
        self.content_urls = [url]

    def _post_get_content(self, responses):
        error_msg = self.errormsg_template.format(id=self.id_list[0])
        for r in responses:
            if not r.text == error_msg:
                continue
            self._empty_handler()
            return

        self.items = 1
        self.titles = [None]
        self.timestamps = [datetime.datetime.fromtimestamp(0)]
        self.content_title = [None]
