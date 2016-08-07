# #!/usr/bin/env python3

import pdb
import imgurpython

from re import sub, match
from os import environ
from os.path import basename, splitext, join

from datetime import datetime
from urllib.parse import urlsplit
from itertools import repeat as rep
from collections import OrderedDict, namedtuple

from .. import PluginBase
from harvester.utils import CustomPath as Path

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
            objs = self._process_single()
        else:
            self.collection = True
            self.particle, collection = self.path_elements[:2]
            if not match("^[A-Za-z0-9]", collection):
                raise Exception("lmao kys")

            collection = sub("[^A-Za-z0-9]+$", "", collection)
            self.collection_id = collection  # after correction

            if self.particle == 'a':
                objs = self._process_a()
            elif self.particle == 'gallery':
                objs = self._process_gallery()

        self.items = len(objs)
        if self.items == 0:
            self.empty = True
            return

        self.id_list = [x.id for x in objs]
        t, ext = zip(*(x.type.split("/") for x in objs))

        assert all(x == "image" for x in t)
        self.items = len(self.id_list)
        self.ext_list = [x if x != "jpeg" else "jpg" for x in ext]
        self.content_urls = [
            x.link.replace("http", "https") for x in objs]
        # self.original_filenames = [basename(x) for x in self.content_urls]
        self.content_filenames = [basename(x) for x in self.content_urls]
        self.content_url_to_id = {
            u: i for u, i in zip(self.content_urls, self.id_list)}
        self.titles = [x.title for x in objs]
        self.timestamps = [
            datetime.fromtimestamp(x.datetime) for x in objs]

    def _process_single(self):
        id_list = [x for x in self.path_elements[0].split(",") if x]

        if self.split.netloc == "i.imgur.com":
            content_id = [splitext(id_list[0])[0]]
            objs = self._api_get_image(content_id)
        else:
            id_list = [splitext(x)[0] for x in id_list]
            self.id_list = list(OrderedDict(zip(id_list, rep(None))))
            objs = self._api_get_image(self.id_list)
        return objs

    def _process_a(self):
        objs = self._api_get_a(self.collection_id)
        return objs

    def _process_gallery(self):
        objs = self._api_get_gallery(self.collection)
        if hasattr(objs, 'images'):
            c = namedtuple('ayylmao', 'id type link title datetime')
            objs = [c(
                id=x['id'], type=x['type'], link=x['link'], title=x['title'],
                datetime=x['datetime']) for x in objs.images]
        elif not objs:
            objs = []
        else:
            objs = [objs]
        return objs

    def get_content(self):
        super().get_content()
        self.collected = True

    def return_path(self):
        if self.collection:
            return Path(self.site, self.particle, self.collection_id)
        else:
            return Path(self.site, 'single')

    def _api_get_image(self, id_list):
        resp = list()
        for id in id_list:
            try:
                resp.append(self.client.get_image(id))
            except imgurpython.helpers.error.ImgurClientError as exc:
                self.failure_ids.append(id)
                self.exceptions.append(exc)
        return resp

    def _api_get_a(self, a_id):
        resp = list()
        try:
            resp = self.client.get_album_images(a_id)
        except imgurpython.helpers.error.ImgurClientError as exc:
            self.failure_ids.append(a_id)
            self.exceptions.append(exc)
        return resp

    def _api_get_gallery(self, a_id):
        resp = list()
        try:
            metadata = self.client.gallery_item(self.collection_id)
            self.collection_title = metadata.title
            resp = self.client.gallery_item(self.collection_id)
        except imgurpython.helpers.error.ImgurClientError as exc:
            self.failure_ids.append(a_id)
            self.exceptions.append(exc)
        return resp
