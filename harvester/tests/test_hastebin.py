#!/usr/bin/env python3

import pdb
import unittest

from harvester.plugins.hastebin import Hastebin


"""
class HastebinTest(unittest.TestCase):

    d = {
        'content_id': 'vohayuzodu',
        'content_extension': None,
        'content_url': 'http://hastebin.com/raw/vohayuzodu',
        'content_filename': 'vohayuzodu',
        'content_hash': "9b4be043ed07098e9ab2d4ea5a86c504",

        'collection': None,
        'collection_id': None,
        'collection_title': None,
    }

    def test_fetch_hastebin_regular_ext(self):
        msg = "http://hastebin.com/vohayuzodu.vala"

        h = Hastebin(msg)
        h.get_content()

        self.assertEquals(h.items, 1)
        d = list(h)[0]

        for k in self.d.keys():
            self.assertEquals(d[k], self.d[k])

    def test_fetch_hastebin_regular_noext(self):
        msg = "http://hastebin.com/vohayuzodu"

        h = Hastebin(msg)
        h.get_content()

        self.assertEquals(h.items, 1)
        d = list(h)[0]

        for k in self.d.keys():
            self.assertEquals(d[k], self.d[k])

    def test_fetch_hastebin_raw(self):
        msg = "http://hastebin.com/raw/vohayuzodu"

        h = Hastebin(msg)
        h.get_content()

        self.assertEquals(h.items, 1)
        d = list(h)[0]

        for k in self.d.keys():
            self.assertEquals(d[k], self.d[k])

    def test_fetch_hastebin_404(self):
        msg = 'http://hastebin.com/ayylmaoo'

        h = Hastebin(msg)
        h.get_content()

        self.assertEquals(h.items, 0)
        self.assertTrue(h.empty)
        self.assertEquals(len(list(h)), 0)
"""

if __name__ == '__main__':
    unittest.main()
