#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib
import unittest

from harvester import harvester


class HastebinTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_hastebin_regular_ext(self):
        msg = "http://hastebin.com/vohayuzodu.vala"
        test_hash = "9b4be043ed07098e9ab2d4ea5a86c504"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_hastebin_regular_noext(self):
        msg = "http://hastebin.com/vohayuzodu"
        test_hash = "9b4be043ed07098e9ab2d4ea5a86c504"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_hastebin_raw(self):
        msg = "http://hastebin.com/raw/vohayuzodu"
        test_hash = "9b4be043ed07098e9ab2d4ea5a86c504"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

if __name__ == '__main__':
    unittest.main()
