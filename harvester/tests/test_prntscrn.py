#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib
import unittest

from harvester import harvester


class PastebinTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_prntscrn(self):
        msg = "http://prntscr.com/5o2enp"
        test_hash = "f6585b7b71fd56e759f6b95ff0e8f20f"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_prntscrn_new(self):
        msg = "http://prntscr.com/bg7sfe"
        test_hash = "3e0a1cb226aed712a95f534a838858eb"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)


if __name__ == '__main__':
    unittest.main()
