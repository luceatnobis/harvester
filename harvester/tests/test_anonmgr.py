#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib
import unittest

from harvester import harvester


class AnonmgrTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_image_share(self):
        msg = "https://anonmgur.com/?f8ed5971ae85d31823ec8557df46f5b5.jpg"
        test_hash = "f29484cf10fe73079c37091b28b77fc4"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_image_direct(self):
        msg = "https://anonmgur.com/up/f8ed5971ae85d31823ec8557df46f5b5.jpg"
        test_hash = "f29484cf10fe73079c37091b28b77fc4"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

if __name__ == '__main__':
    unittest.main()
