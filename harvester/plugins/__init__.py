#!/usr/bin/env python3

import hashlib
import datetime
import grequests

from itertools import zip_longest as zip
from collections import OrderedDict

from pytz import timezone

__all__ = ["imgur", "pastebin"]


class PluginBase:

    def __init__(self):
        self.collected = False
        self.collection = None 
        self.collection_id = None 
        self.collection_title = None
        self.archival_timestamp = datetime.datetime.now()

        self.hashes = list()

    def _chunks(self, l, n=50):
        for i in range(0, len(l), n):
            yield l[i:i+n]

    def _hash(self, content):
        return hashlib.md5(content).hexdigest()

    def get_content(self):
        responses = list()
        for chunk in self._chunks(self.content_urls):
            rs = (grequests.get(x) for x in chunk)
            responses.extend(grequests.map(rs))

        responses.sort(key=lambda x: self.content_urls.index(x.url))

        self.contents = [x.content for x in responses]
        self.hashes = [self._hash(x.content) for x in responses]

        return self._post_get_content(responses)

    def _post_get_content(self, responses):
        pass

    def __iter__(s):

        if not s.collected:
            s.get_content()

        for d, e, cu, t, ct, f, h, c in zip(
            s.id_list, s.ext_list, s.content_urls, s.titles,
            s.timestamps, s.original_filenames, s.hashes, s.contents
        ):

            yield ContentObj(**{
                'site': s.site,
                'content_id': d,
                'content_url': cu,
                'content_hash': h,
                'content_title': t,
                'content_timestamp': ct,
                'original_url': s.original_url,
                'original_filename': f,
                'original_extension': e,
                'archived_at': s.archival_timestamp,
                'collection': s.collection,
                'collection_id': s.collection_id,
                'collection_title': s.collection_title,
                'content': c,
            })


class ContentObj(OrderedDict):
    field_order = (
        'site', 'content_id', 'content_url', 'content_hash', 'content_title',
        'content_timestamp', 'original_url', 'original_filename',
        'original_filename','original_extension', 'archived_at',
        'collection', 'collection_id', 'collection_title'
    )
    non_dict = ('content', )

    def __init__(self, **kwargs):
        assert set(kwargs.keys()) == set(self.field_order + self.non_dict)

        super().__init__()
        for i, f in enumerate(self.field_order):
            self.__setitem__(f, kwargs.get(f))

        for i, f in enumerate(self.non_dict):
            setattr(self, f, kwargs.get(f))

    def __repr__(self):
        return '{' + ", ".join("{k}: {v}".format(k=k, v=v) for k, v in [(f,
            self.get(f)) for f in self.field_order]) + '}'
