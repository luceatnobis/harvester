#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib
import unittest

from harvester import harvester


class AnonywsTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_image_link(self):
        msg = "http://anony.ws/image/JC6u"
        test_hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_image_raw(self):
        msg = "http://anony.ws/i/2016/06/16/carlton.png"
        test_hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_image_md(self):
        msg = "http://anony.ws/i/2016/06/16/carlton.md.png"
        test_hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_image_th(self):
        msg = "http://anony.ws/i/2016/06/16/carlton.th.png"
        test_hash = "3c1a8ef650f3c3c3c2f4dd115931c0ca"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

if __name__ == '__main__':
    unittest.main()
