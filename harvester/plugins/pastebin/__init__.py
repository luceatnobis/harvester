#!/usr/bin/env python3

import pdb
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlsplit

from dateutil import parser
from dateutil.tz import gettz

from .. import PluginBase

class Pastebin(PluginBase):

    site = 'pastebin'

    def __init__(self, url):
        super().__init__()
        self.original_url = url
        split = urlsplit(url)
        elements = [x for x in split.path.split('/') if x]

        # http://pastebin.com/Vcz07KuK  regular
        # http://pastebin.com/raw/Vcz07KuK  new raw
        # http://pastebin.com/raw.php?i=Vcz07KuK  old raw

        if len(elements) == 2 and elements[0] == 'raw':
            paste_id = elements[1]
        elif elements[0] == 'raw.php':
            params = {k: v for (k, v) in (
                kv.split('=') for kv in split.query.split('&'))}
            paste_id = params.get('i')
        else:
            paste_id = elements[0]

        raw_url = "http://pastebin.com/raw/{id}".format(id=paste_id)
        metadata_url = "http://pastebin.com/{id}".format(id=paste_id)

        self.ext_list = [None]
        self.id_list = [paste_id]
        self.content_filenames = [paste_id]
        self.content_urls = [raw_url, metadata_url]
        
    def _post_get_content(self, responses):
        if not all(x.ok for x in responses):
            self._empty_handler()
            return

        self.items = 1
        self.content_urls.pop()
        self.hashes.pop()

        m = self.contents.pop()
        s = BeautifulSoup(m, "html5lib")
        ts = s.find('div', {'class': 'paste_box_line2'}).span.get('title')
        ts = parser.parse(ts, tzinfos={'CDT': gettz("US/Central")})
        self.timestamps = [ts.astimezone(gettz("UTC"))]

        self.titles = [s.h1.text]
        self.collected = True
