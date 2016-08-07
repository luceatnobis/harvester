#!/usr/bin/env python3.5

import pdb
import hashlib
import datetime
import grequests

from itertools import count
from collections import OrderedDict

from pytz import timezone

from harvester.utils import CustomPath as Path

__all__ = ["imgur", "pastebin"]


class PluginBase:

    def __init__(self):
        self.empty = False
        self.collected = False
        self.collection = None
        self.collection_id = None
        self.collection_title = None
        self.archival_timestamp = datetime.datetime.now(timezone('utc'))

        self.hashes = list()
        self.contents = list()

        self.exceptions = list()
        self.failure_ids = list()

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

        """
        for r in responses:
            c = r.content
            if 'text/plain' in r.headers.get('content-type', ""):
                c = c.replace(b"\r\n", b"\n")
            self.contents.append(c)
        """

        self.contents = [r.content for r in responses]
        self.hashes = [self._hash(x) for x in self.contents]
        return self._post_get_content(responses)

    def _post_get_content(self, responses):
        pass

    def return_path(self):
        return Path(self.site)

    def _empty_handler(self):
        self.items = 0
        self.empty = True
        self.failure_ids = [self.id_list]
        return

    def __iter__(s):

        if s.empty:
            return list()

        if not s.collected:
            s.get_content()

        if s.empty:  # sometimes we need to know before and after collecting
            return list()  # though i should probably find a way to avoid that

        for d, e, cu, t, ct, f, h, c, i in zip(
            s.id_list, s.ext_list, s.content_urls, s.titles,
            s.timestamps, s.content_filenames, s.hashes, s.contents, count(1)
        ):
            yield ContentObj(**{
                'site': s.site,
                'content_id': d,
                'content_url': cu,
                'content_hash': h,
                'content_title': t,
                'content_timestamp': int(ct.timestamp()),
                'content_filename': f,
                'content_extension': e,
                'content_index': i,
                'original_url': s.original_url,
                'archived_at': int(s.archival_timestamp.timestamp()),
                'collection': s.collection,
                'collection_id': s.collection_id,
                'collection_title': s.collection_title,
                'content': c,
            })


class ContentObj(OrderedDict):

    field_order = (
        'site', 'content_id', 'content_url', 'content_hash', 'content_title',
        'content_timestamp', 'content_filename', 'content_extension',
        'content_index', 'original_url', 'archived_at', 'collection',
        'collection_id', 'collection_title',
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
        return '{' + ", ".join("{k}: {v}".format(k=k, v=v) for k, v in [
            (f, self.get(f)) for f in self.field_order]) + '}'
