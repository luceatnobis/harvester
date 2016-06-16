#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import hashlib
import unittest

from harvester import harvester


class MixtapeTest(unittest.TestCase):

    def setUp(self):
        self.nick = "test"
        self.chan = '#brotherBot'
        self.mask = "brotherBox!~brotherBo@unaffiliated/brotherbox"
        self.h = harvester.HarvesterBot

    def test_fetch_spit_paste_share(self):
        msg = "https://spit.mixtape.moe/view/39598db9"
        test_hash = "2b14f6a69199243f570031bf94865bb6"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_spit_paste_raw(self):
        msg = "https://spit.mixtape.moe/view/raw/39598db9"
        test_hash = "2b14f6a69199243f570031bf94865bb6"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)
        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

    def test_fetch_my_file(self):
        msg = "https://my.mixtape.moe/egojmm.mp3"
        test_hash = "946a3ba94aac53ef30415eaa489bcecb"

        c = self.h._retrieve_content(self.h, self.mask, msg, self.chan)

        md5 = hashlib.md5()
        md5.update(c[0]['content'])
        self.assertEqual(md5.hexdigest(), test_hash)

if __name__ == '__main__':
    unittest.main()
