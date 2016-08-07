#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib
import unittest

"""
from harvester import harvester


class BPasteTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_bpaste_regular(self):
        msg = "https://bpaste.net/show/426fe62985e3"
        test_hash = "3d44a1c26120298fae05b3809bcb4f78"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_bpaste_raw(self):
        msg = "https://bpaste.net/raw/426fe62985e3"
        test_hash = "3d44a1c26120298fae05b3809bcb4f78"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)
"""

if __name__ == '__main__':
    unittest.main()
