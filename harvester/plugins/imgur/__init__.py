#!/usr/bin/env python3

import pdb
import grequests
import imgurpython

from re import sub, match
from os import environ
from os.path import basename, splitext, join

from datetime import datetime
from urllib.parse import urlsplit
from itertools import repeat as rep
from collections import OrderedDict, namedtuple

from .. import PluginBase

from importlib.machinery import SourceFileLoader
key_imgur = SourceFileLoader("key_imgur.py", join(
    environ['HOME'], ".harvester/key_imgur.py")).load_module()


class Imgur(PluginBase):

    site = 'imgur'

    def __init__(self, url):
        super().__init__()
        self.client = imgurpython.ImgurClient(
            key_imgur.cred['client-id'], key_imgur.cred['client-secret']
        )
        self.original_url = url

        self.split = urlsplit(url)
        self.path_elements = [x for x in self.split.path.split("/") if x]

        if len(self.path_elements) == 1:
            self._process_single()
        else:
            self.collection = True
            self.particle, collection = self.path_elements[:2]
            if not match("^[A-Za-z0-9]", collection):
                raise Exception("lmao kys")

            collection = sub("[^A-Za-z0-9]+$", "", collection)
            self.collection_id = collection  # after correction

            if self.particle == 'a':
                self._process_a()
            elif self.particle == 'gallery':
                self._process_gallery()

        self.id_list = [x.id for x in self._objs]
        t, ext = zip(*(x.type.split("/") for x in self._objs))

        assert all(x == "image" for x in t)
        self.items = len(self.id_list)
        self.ext_list = [x if x != "jpeg" else "jpg" for x in ext]
        self.content_urls = [
            x.link.replace("http", "https") for x in self._objs]
        self.original_filenames = [basename(x) for x in self.content_urls]
        self.content_url_to_id = {
            u: i for u, i in zip(self.content_urls, self.id_list)}
        self.titles = [x.title for x in self._objs]
        self.timestamps = [
            datetime.fromtimestamp(x.datetime) for x in self._objs]

    def _process_single(self):
        filenames = [x for x in self.path_elements[0].split(",") if x]

        if self.split.netloc == "i.imgur.com":
            content_id = splitext(filenames[0])[0]
            self._objs = [self.client.get_image(content_id)]
        else:
            filenames = [splitext(x)[0] for x in filenames]
            self.id_list = list(OrderedDict(zip(filenames, rep(None))))
            self._objs = [self.client.get_image(i) for i in self.id_list]

    def _process_a(self):
        metadata = self.client.get_album(self.collection_id)
        self.collection_title = metadata.title
        self._objs = [
            x for x in self.client.get_album_images(self.collection_id)]

    def _process_gallery(self):
        objs = self.client.gallery_item(self.collection_id)
        if hasattr(objs, 'images'):
            c = namedtuple('ayylmao', 'id type link title datetime')
            objs = [c(
                id=x['id'], type=x['type'], link=x['link'], title=x['title'],
                datetime=x['datetime']) for x in objs.images]
        else:
            objs = [objs]
        self._objs = objs

    def get_content(self):
        super().get_content()
        self.collected = True

    def return_path(self):
        if self.collection:
            return join(self.site, self.particle, self.collection_id)
        else:
            return join(self.site, 'single')
