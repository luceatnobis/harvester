#!/usr/bin/env python3

import pdb
import unittest
from datetime import datetime

from harvester.plugins.pastebin import Pastebin


class PastebinTest(unittest.TestCase):

    def setUp(self):
        self.now = datetime.now()
        self.test_dict = {
            'site': 'pastebin',
            'archived_at': int(self.now.timestamp()),
            'content_title': 'Untitled',
            'content_id': 'Vcz07KuK',
            'content_url': 'http://pastebin.com/raw/Vcz07KuK',
            'content_hash': '6f200af60b8ad355f7757b8f0e3efb00',
            # LF hash
            # 'content_hash': 'e906a2453c38c4b106d113ca1cb689f0',
            'collection': None,
        }

    def test_pastebin_fetch_regular(self):
        msg = "http://pastebin.com/Vcz07KuK"

        klass = Pastebin(msg)
        klass.archival_timestamp = self.now
        klass.get_content()

        self.assertFalse(klass.empty)
        self.assertEquals(klass.exceptions, [])
        self.assertEquals(klass.items, 1)
        d = list(klass)[0]

        for k, v in self.test_dict.items():
            self.assertEquals(d[k], v)

    def test_pastebin_fetch_new_raw(self):
        msg = "http://pastebin.com/raw/Vcz07KuK"

        klass = Pastebin(msg)
        klass.archival_timestamp = self.now
        klass.get_content()

        self.assertFalse(klass.empty)
        self.assertEquals(klass.exceptions, [])
        self.assertEquals(klass.items, 1)
        d = list(klass)[0]

        for k, v in self.test_dict.items():
            self.assertEquals(d[k], v)

    def test_pastebin_fetch_old_raw(self):
        msg = "http://pastebin.com/raw.php?i=Vcz07KuK"

        klass = Pastebin(msg)
        klass.archival_timestamp = self.now
        klass.get_content()

        self.assertFalse(klass.empty)
        self.assertEquals(klass.exceptions, [])
        self.assertEquals(klass.items, 1)
        d = list(klass)[0]

        for k, v in self.test_dict.items():
            self.assertEquals(d[k], v)

    def test_pastebin_404(self):
        msg = "http://pastebin.com/thisisinvalid"

        klass = Pastebin(msg)
        klass.get_content()

        self.assertTrue(klass.empty)
        self.assertEquals(klass.items, 0)
        self.assertEquals(list(klass), [])

if __name__ == '__main__':
    unittest.main()
