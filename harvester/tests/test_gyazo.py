#!/usr/bin/env python3

import hashlib
import unittest

'''
from harvester import harvester


class GyazoTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_gyazo_share(self):
        msg = "https://gyazo.com/fc12a9bb2a4b92d1debef49b8279371f"
        test_hash = "fc12a9bb2a4b92d1debef49b8279371f"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_gyazo_raw(self):
        msg = "https://i.gyazo.com/fc12a9bb2a4b92d1debef49b8279371f.png"
        test_hash = "fc12a9bb2a4b92d1debef49b8279371f"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_gyazo_cache(self):
        msg = "https://cache.gyazo.com/fc12a9bb2a4b92d1debef49b8279371f.png"
        test_hash = "fc12a9bb2a4b92d1debef49b8279371f"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)
'''

if __name__ == '__main__':
    unittest.main()
