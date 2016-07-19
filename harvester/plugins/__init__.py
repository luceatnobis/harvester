#!/usr/bin/env python3

import hashlib
import datetime

from itertools import zip_longest as zip
from collections import OrderedDict

from pytz import timezone

__all__ = ["imgur"]


class PluginBase:

    def __init__(self):
        self.collected = False
        self.collection_title = False
        self.timestamp = datetime.datetime.now(timezone('UTC'))

    def _chunks(self, l, n=50):
        for i in range(0, len(l), n):
            yield l[i:i+n]

    def _hash(self, content):
        return hashlib.md5(content).hexdigest()

    def __iter__(s, id_list=None):

        for d, e, cu, t, f, h in zip(
            s.id_list, s.ext_list, s.content_urls, s.titles,
            s.original_filenames, s.hashes,
        ):

            yield ContentObj(**{
                'path': s.return_path(),
                'content': s.id_to_content[d],
                'timestamp': s.timestamp,
                'site': s.site,
                'collection': s.collection,
                'content_id': d,
                'content_url': cu,
                'content_hash': h,
                'content_title': t,
                'original_url': s.original_url,
                'original_filename': f,
                'original_extension': e,
            })

    def get_content(self):
        raise NotImplementedError


class ContentObj(OrderedDict):
    field_order = (
        'timestamp', 'site', 'collection', 'content_id', 'content_url',
        'content_hash', 'content_title', 'original_url', 'original_filename',
        'original_extension'
    )
    non_dict = ('path', 'content')

    def __init__(self, **kwargs):
        assert set(kwargs.keys()) == set(self.field_order + self.non_dict)

        super().__init__()
        for i, f in enumerate(self.field_order):
            self.__setitem__(f, kwargs.get(f))

        for i, f in enumerate(self.non_dict):
            setattr(self, f, kwargs.get(f))
