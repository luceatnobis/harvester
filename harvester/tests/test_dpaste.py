#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib
import unittest

from harvester import harvester


class DPasteTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_dpaste_regular(self):
        msg = "http://dpaste.com/2E0H71M"
        test_hash = "e0e5bd63c9d415c7fb84eecaa74c78fc"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_dpaste_raw(self):
        msg = "http://dpaste.com/2E0H71M.txt"
        test_hash = "e0e5bd63c9d415c7fb84eecaa74c78fc"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

if __name__ == '__main__':
    unittest.main()
