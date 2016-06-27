#!/usr/bin/env python3

import pdb
import hashlib
import requests

from .. import PluginBase 
from urllib.parse import urlsplit


class CubeUpload(PluginBase):

    site = 'cubeupload'
    raw_base_url = "http://i.cubeupload.com/%s"

    def __init__(self, url):
        self.original_url = url
        self.collection = None
        self.collection_url = None
        self.filename = urlsplit(self.original_url).path.split('/')[-1]
        self.original_filename, self.extension = self.filename.split('.')
        self.content_url = self.raw_base_url % self.filename

        self.id_list = [self.original_filename]
        self.ext_list = [self.extension]

    def get_identifiers(self):
        return self.id_list

    def get_content(self):
        if not hasattr(self, 'content'):
            self.store_content()
        return self.content

    def store_content(self):
        response = requests.get(self.content_url)

        if not response.ok:
            raise Exception("lol i dunno")

        self.items = 1
        self.content_list = [response.content]
        self.hashes = [hashlib.md5(response.content).hexdigest()]
